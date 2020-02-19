# (not with this task (we use MySql) ) 
# (if there is db not supported indexing on foreign keys) 
# 0. on foreign key
ALTER TABLE Students ADD INDEX(room_id);

# 1. add index on students name (becouse in most cases we serching by people by name)
ALTER TABLE Students ADD INDEX(name);

# (not with this in data) 
# 2. add index on rooms name (if we have come usefull information in rooms name) 
ALTER TABLE Rooms ADD INDEX(name);

# 3. add index students sex (if there is a dormitory db (or we make some statistics quite often) ) 
ALTER TABLE Students ADD INDEX(sex);