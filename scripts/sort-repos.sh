
# Generate file repo-stargazer.csv
# iterate trough repos

for i in `find  files/users -type f `
do
 [ ! -f  "files/sort-users/`basename $i`" ] && cat "$i"  | jq ".[]" | jq -s   "sort_by (.updated_at)"  > files/sort-users/`basename "$i"`
done




