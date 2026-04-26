-- ============================================================
-- Remote Work Analytics SQL Queries
-- Author: Yousuf Patel | BMW Collaboration Project
-- Table: workforce (matches synthetic_workforce_data.csv schema)
-- ============================================================


-- 1. Adoption rate by country
SELECT
    country,
    work_mode,
    COUNT(*)                                          AS employee_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY country), 2) AS pct_of_country
FROM workforce
GROUP BY country, work_mode
ORDER BY country, pct_of_country DESC;


-- 2. Average productivity and satisfaction by work mode
SELECT
    work_mode,
    COUNT(*)                                  AS headcount,
    ROUND(AVG(productivity_score), 2)         AS avg_productivity,
    ROUND(AVG(satisfaction_score), 2)         AS avg_satisfaction,
    ROUND(AVG(commute_hours_per_week), 2)     AS avg_commute_hours_pw
FROM workforce
GROUP BY work_mode
ORDER BY avg_productivity DESC;


-- 3. Country × work mode KPI matrix
SELECT
    country,
    work_mode,
    COUNT(*)                                               AS employees,
    ROUND(AVG(productivity_score), 2)                     AS avg_productivity,
    ROUND(AVG(satisfaction_score), 2)                     AS avg_satisfaction,
    ROUND(SUM(annual_office_cost_saving_eur) / 1000, 1)   AS total_savings_k_eur
FROM workforce
GROUP BY country, work_mode
ORDER BY country, work_mode;


-- 4. Productivity by department and work mode
SELECT
    department,
    work_mode,
    COUNT(*)                              AS headcount,
    ROUND(AVG(productivity_score), 2)    AS avg_productivity
FROM workforce
GROUP BY department, work_mode
ORDER BY department, avg_productivity DESC;


-- 5. Total annual cost savings by country
SELECT
    country,
    ROUND(SUM(annual_office_cost_saving_eur), 0)      AS total_savings_eur,
    ROUND(AVG(annual_office_cost_saving_eur), 0)      AS avg_savings_per_employee_eur,
    SUM(CASE WHEN work_mode = 'Fully Remote' THEN 1 ELSE 0 END) AS fully_remote_count
FROM workforce
GROUP BY country
ORDER BY total_savings_eur DESC;


-- 6. High-performing remote segment (productivity > 8 AND remote/hybrid)
SELECT
    country,
    department,
    job_level,
    work_mode,
    COUNT(*)                              AS headcount,
    ROUND(AVG(productivity_score), 2)    AS avg_productivity,
    ROUND(AVG(satisfaction_score), 2)    AS avg_satisfaction
FROM workforce
WHERE
    work_mode IN ('Fully Remote', 'Hybrid')
    AND productivity_score > 8.0
GROUP BY country, department, job_level, work_mode
HAVING COUNT(*) >= 3
ORDER BY avg_productivity DESC;


-- 7. Meeting load vs productivity correlation
SELECT
    CASE
        WHEN meetings_per_week <= 5  THEN 'Low (≤5)'
        WHEN meetings_per_week <= 10 THEN 'Medium (6-10)'
        WHEN meetings_per_week <= 15 THEN 'High (11-15)'
        ELSE 'Very High (15+)'
    END                                   AS meeting_load,
    work_mode,
    COUNT(*)                              AS headcount,
    ROUND(AVG(productivity_score), 2)    AS avg_productivity
FROM workforce
GROUP BY meeting_load, work_mode
ORDER BY meeting_load, work_mode;
