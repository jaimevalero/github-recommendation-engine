
# Generate file repo-stargazer.csv
# iterate trough repos
source .credentials
#cd /Users/jaimevalerodebernabe/git/github-recommendation-engine/scripts/files

cat repo-stargazer.csv | cut -d, -f2-100 | tr ',' '\n' | sort -du | tail -9600  | sort -r | while read MY_USER
do
  [  -f  "/Users/jaimevalerodebernabe/git/github-recommendation-engine/scripts/files/$MY_USER.json" ] && [ ! -f  "files/starred/$MY_USER" ] &&   curl -s -u $CRED "https://api.github.com/users/$MY_USER/starred?per_page=500"  | jq -r '.[]|.full_name' > "files/starred/$MY_USER"

 echo "$MY_USER"
done


