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

db.papers_keywords.aggregate([
        {$group: {_id: "$paper_id", fields: {$addToSet: "$field_id"}}},
        {$out: "tmpPapers"}
    ], { allowDiskUse: true });

db.tmpPapers.find().noCursorTimeout().forEach(function(paper){
    var of_interest = false;
    db.fields_of_study.find({
        _id: {$in: paper.fields},
        $or: [
            {computer_science: {$exists: true}}, 
            {physics: {$exists: true}}, 
            {materials_science: {$exists: true}}
        ]
    }).noCursorTimeout().forEach(function(field){
        if(field.computer_science){
            paper['computer_science'] = true;
        }
        if(field.physics){
            paper['physics'] = true;
        }
        if(field.materials_science){
            paper['materials_science'] = true;
        }
        of_interest = true;
    });
    if(of_interest){
        delete paper.fields;
        db.paper_domains.insert(paper);
    }
});

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
