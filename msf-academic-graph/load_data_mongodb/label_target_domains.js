/* Add a collection with the list of the domains of 
 * interest for the task with their respective 'field_id' 
 * in the MS Academic Graph */
db.domain_fields.insert({ "_id" : "0271BC14", "name" : "computer_science" });
db.domain_fields.insert({ "_id" : "073B64E4", "name" : "physics" });
db.domain_fields.insert({ "_id" : "0B7A44E7", "name" : "materials_science" });

/* Labels fields of study in the collection 'fields_of_study' 
 * with one or more of three domains, these domains are 
 * computer_science
 * physics
 * materials_science 
 *
 * Example:
 *
    {
        "_id" : "00F7166F",
        "field_name" : "Electrical length",
        "computer_science" : true,
        "physics" : true,
        "materials_science" : true
    }
 */
function label_target_fields(parent_id, field){
    db.field_of_study_hierarchy.find({parent_id: parent_id}).forEach(function(doc){
        var new_field = {};
        new_field[field.name] = true;
        db.fields_of_study.update({_id: doc.child_id}, {$set: new_field});
        label_target_fields(doc.child_id, field);
    });
}
db.domain_fields.find().forEach(function(target_fields){
    for(var t in target_fields){
        label_target_fields(target_fields[t]._id, target_fields[t]);
    }
});


/* Creates a colletion named 'paper_domains' with the ids
 * of the papers labeled with the target domains.
 *
 * Examples:
 *
        { "_id" : "0000002B", "computer_science" : true }
        { "_id" : "0000003A", "physics" : true }
        { "_id" : "000000BB", "physics" : true }
        { "_id" : "000000BE", "computer_science" : true, "physics" : true, "materials_science" : true }
        { "_id" : "00000116", "physics" : true }
*/
db.papers_keywords.aggregate([
        {$group: {_id: "$field_id", papers: {$addToSet: "$paper_id"}}},
        {$out: "tmpFieldsPapers"}
    ], { allowDiskUse: true });
db.fields_of_study.find().noCursorTimeout().forEach(function(field){
    var field_id = field._id;
    delete field.field_name;
    delete field._id;
    db.tmpFieldsPapers.update({_id: field_id}, {$set: field});
});
db.tmpFieldsPapers.aggregate([
    {$match: {$or: [{computer_science: {$exists: true}}, 
                 {physics: {$exists: true}}, 
                 {materials_science: {$exists: true}}]
             }
    },
    {$unwind: "$papers"},
    {$group: {_id: "$papers", 
                 computer_science: {$push: "$computer_science"},
                 physics: {$push: "$physics"},
                 materials_science: {$push: "$materials_science"}
             }
    },
    {$project: {_id: 1, 
                   computer_science: {$cond: [{$size: "$computer_science"}, true, false]},
                   physics: {$cond: [{$size: "$physics"}, true, false]},
                   materials_science: {$cond: [{$size: "$materials_science"}, true, false]} 
               }
    },
    {$out: "paper_domains"}
], { allowDiskUse: true }); 
db.paper_domains.update({computer_science: false}, {$unset: {computer_science: ""}}, {multi: true});
db.paper_domains.update({physics: false}, {$unset: {physics: ""}}, {multi: true});
db.paper_domains.update({materials_science: false}, {$unset: {materials_science: ""}}, {multi: true});

/* Creates a collection named 'keywords' with all the keywords
 * labeled with the target domains. 
 *
 * Examples:
 *
        { "_id" : "steam turbine efficiency", "count" : 1, "physics" : true }
        { "_id" : "external bus interface", "count" : 1, "computer_science" : true }
        { "_id" : "outscatter", "count" : 1, "computer_science" : true }
 */
db.papers_keywords.aggregate([
        {$group: {_id: "$keyword_name", count: {$sum: 1}, fields: {$addToSet: "$field_id"}}},
        {$out: "tmpKeywords"}
    ], {allowDiskUse: true});
db.tmpKeywords.find().noCursorTimeout().forEach(function(keyword){
    var of_interest = false;
    db.fields_of_study.find({
        _id: {$in: keyword.fields},
        $or: [
            {computer_science: {$exists: true}}, 
            {physics: {$exists: true}}, 
            {materials_science: {$exists: true}}
        ]
    }).noCursorTimeout().forEach(function(field){
        if(field.computer_science){
            keyword['computer_science'] = true;
        }
        if(field.physics){
            keyword['physics'] = true;
        }
        if(field.materials_science){
            keyword['materials_science'] = true;
        }
        of_interest = true;
    });
    if(of_interest){
        delete keyword.fields;
        db.keywords.insert(keyword);
    }
});
db.tmpKeywords.find().noCursorTimeout().forEach(function(keyword){
    var of_interest = false;
    db.fields_of_study.find({
        _id: {$in: keyword.fields},
        computer_science: {$exists: false}, 
        physics: {$exists: false}, 
        materials_science: {$exists: false}
    }).noCursorTimeout().forEach(function(field){
        of_interest = true;
    });
    if(of_interest){
        delete keyword.fields;
        db.keywords_not_of_interest.insert(keyword);
    }
});
