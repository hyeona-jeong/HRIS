DELIMITER //

CREATE TRIGGER UPDATE_FORUM_EDITDATE
BEFORE UPDATE ON forum
FOR EACH ROW
BEGIN
  SET NEW.edit_date = CURRENT_TIMESTAMP;
END;

//

DELIMITER ;