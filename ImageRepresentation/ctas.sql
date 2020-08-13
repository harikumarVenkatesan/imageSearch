create table image_search.image(
   image_id INT NOT NULL AUTO_INCREMENT,
   image_path VARCHAR(100) NOT NULL,
   PRIMARY KEY ( image_id, image_path )
);

