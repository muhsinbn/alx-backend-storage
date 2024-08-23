-- This stored procedure computes and stores the average weighted score for a student.
-- It takes one input parameter, user_id, which is the ID of the user whose average weighted score will be computed.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;

    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_weighted_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    IF total_weight > 0 THEN
        SET total_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET total_weighted_score = 0;
    END IF;

    UPDATE users
    SET users.average_score = total_weighted_score
    WHERE users.id = user_id;
END $$
DELIMITER ;
