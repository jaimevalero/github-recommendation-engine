
# Generate file repo-stargazer.csv
# iterate trough repos
source .credentials
#cd /Users/jaimevalerodebernabe/git/github-recommendation-engine/scripts/files
echo "Calculating repos"
cat files/all_repos | cut -d' ' -f1 | sort | uniq -c | sort -k1 -n -r | head -7500 | awk '{ print $2}' | while read repo 
do
  echo $repo
curl -s  "https://$CRED@api.github.com/repos/$repo" | jq '. |[ { description, "avatar_url": .owner["avatar_url"] }]'  | jq -c -r '.[0]|.avatar_url,.description'  | tr -d ,  |tr \\n ,  | sed -e "s@^@${repo},@g"  |   sed -e 's@,$@@g' >> stared-descriptions.csv
   
done


