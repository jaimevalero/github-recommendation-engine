
# Generate file repo-stargazer.csv
# iterate trough repos
source .credentials
> repo-stargazer.csv
cat ../TopStaredRepositories.csv | grep -v Username | cut -d, -f1-2 | tr , /  | while read REPO 
do
  echo $REPO curl "'https://$CRED@api.github.com/repos/$REPO/stargazers'"
  # get user that stared it
  curl https://$CRED@api.github.com/repos/$REPO/stargazers | jq -r -c '.[].login' | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g'| tr ' ' , | sed -e "s@^@${REPO},@g"  >> repo-stargazer.csv
done

