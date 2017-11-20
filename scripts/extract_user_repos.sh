
# Generate file repo-stargazer.csv
# iterate trough repos
source .credentials
cat repo-stargazer.csv | cut -d, -f2-100 | tr ',' '\n' | sort -du | head -20000| while read MY_USER
do
  # get user that stared it
 echo "$MY_USER"
 [ ! -f  "files/$MY_USER.json" ] && curl -s -H "Accept: application/vnd.github.mercy-preview+json" "https://$CRED@api.github.com/users/$MY_USER/repos" | jq . > files/$MY_USER.json
done


# Check file are correct
cd files
for i in `ls ` ; do  echo $i:`cat $i | jq . 1>/dev/null ; echo $?`: ; done | grep -v :0:
