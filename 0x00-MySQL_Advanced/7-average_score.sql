-- stored procedure that computes and store the average score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE avg_score INT DEFAULT 0;

    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET users.average_score = avg_score
    WHERE users.id = user_id;
END $$
DELIMITER ;
