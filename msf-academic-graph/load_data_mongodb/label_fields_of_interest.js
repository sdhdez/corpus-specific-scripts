function label_target_fields(parent_id, field){
    db.field_of_study_hierarchy.find({parent_id: parent_id}).forEach(function(doc){
        var new_field = {};
        new_field[field.name] = true;
        db.fields_of_study.update({_id: doc.child_id}, {$set: new_field});
        label_target_fields(doc.child_id, field);
    });
}

db.domain_fields.find(function(target_fields){
    for(var t in target_fields){
        label_target_fields(target_fields[t]._id, target_fields[t]);
    }
});
