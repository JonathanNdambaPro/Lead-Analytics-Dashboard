WITH unpivoted_and_weekly AS (
  SELECT
    DATE_TRUNC('week', date) AS semaine,
    type_evenement,
    date
  FROM (
    UNPIVOT DELTA_SCAN('{{ delta_table_path }}')
    ON {% for col in date_cols %}{{ col }}{% if not loop.last %},
           {% endif %}{% endfor %}
    INTO
    NAME type_evenement
    VALUE date
  )
  WHERE date IS NOT NULL
)

PIVOT unpivoted_and_weekly
ON type_evenement
USING COUNT(date)
GROUP BY semaine
ORDER BY semaine;
