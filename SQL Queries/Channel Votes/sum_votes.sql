-- SELECT *
-- FROM opros;

-- SELECT *
-- FROM channel;

SELECT DISTINCT CONCAT(MONTHNAME(q.date_quiz), ' ', YEAR(q.date_quiz)) AS 'Month Year',
				c.name_channel AS 'Channel', 
	(
		SELECT COALESCE(SUM(temp_q.nom_operator), 0)
		FROM quiz temp_q
		WHERE temp_q.channels LIKE CONCAT('%', c.id_channel, '%') AND MONTHNAME(temp_q.date_quiz) = MONTHNAME(q.date_quiz)
    ) AS 'count'
FROM channel c, quiz q
ORDER BY q.date_quiz, c.name_channel;