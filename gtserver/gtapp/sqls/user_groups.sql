--Listet alle Benutzer und ihre Zugehörige Gruppe auf
SELECT auth_user.username Benutzer, auth_group.name Gruppe
FROM auth_user, auth_group, auth_user_groups
WHERE auth_user.id = auth_user_groups.user_id
AND auth_group.id = auth_user_groups.group_id
ORDER BY auth_user.username