-- Creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD weightedScore INT NOT NULL;
    ALTER TABLE users ADD totalWeight INT NOT NULL;

    UPDATE users
    SET weightedScore = (
        SELECT SUM(corrections.score * projects.weight)
        FROM corrections INNER JOIN projects
        ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );

    UPDATE users
    SET totalWeight = (
        SELECT SUM(projects.weight)
        FROM corrections INNER JOIN projects
        ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );

    UPDATE users
    SET users.average_score = IF(users.totalWeight = 0, 0, users.weightedScore / users.totalWeight);

    ALTER TABLE users
        DROP COLUMN weightedScore;
    ALTER TABLE users
        DROP COLUMN totalWeight;
END $$
DELIMITER ;
