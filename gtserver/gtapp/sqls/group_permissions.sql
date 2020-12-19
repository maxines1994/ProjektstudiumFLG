--Auswertung: Gruppen und ihre Rechte
SELECT auth_group.name_de Gruppe, auth_permission.name Recht
FROM auth_group, auth_permission, auth_group_permissions
WHERE auth_group.id = auth_group_permissions.group_id
AND auth_permission.id = auth_group_permissions.permission_id