-- procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE weightedScore INT DEFAULT 0;
    DECLARE totalWeight INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight)
    INTO weightedScore
    FROM corrections INNER JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight) INTO totalWeight
    FROM corrections INNER JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    IF totalWeight = 0 THEN
        UPDATE users
        SET users.average_score = 0
        WHERE users.id = user_id;
    ELSE
        UPDATE users
        SET users.average_score = weightedScore / totalWeight
        WHERE users.id = user_id;
    END IF;
END $$
DELIMITER ;
