--Auswertung: TaskTypes sortiert nach Gruppe
SELECT g.name Gruppe, t.id TaskTypeID, t.title Titel, t.description Beschreibung, t.status_model 'Model für Status', t.task_model 'Model für Task', t.view_url 'Redirect-Template', t.template_kwargs 'Kwargs für Redirect'
FROM gtapp_tasktype t, auth_group g
WHERE t.group_id = g.id
ORDER BY Gruppe