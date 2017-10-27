
**Demo site https://github-recommendation.herokuapp.com/views/index.html?busqueda=jaimevalero**


# Github recomendation system 


  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/20c8cb7ed93a4064b4aaf1420eae5880)](https://www.codacy.com/app/jaimevalero78/github-recommendation-engine?utm_source=github.com&utm_medium=referral&utm_content=jaimevalero/github-recommendation-engine&utm_campaign=badger)  [![BCH compliance](https://bettercodehub.com/edge/badge/jaimevalero/github-recommendation-engine?branch=master)](https://bettercodehub.com/) 
  
  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)



Get famous repos that are similar to yours.
This system parses an user repos, label, names descriptipn, and it displays those repos that have resemblance with it.

The idea here is to find and learn new technologies, that are similar to the ones you already master, making a smooth learning curve.

Internally, it uses an euclidean distance matrix, calculated for 800 labels, where each label is a binary [0,1] dimension, to find similar repos.

TODO: Use a filter based recomendation system, with like/dislike buttons.


Repo list from https://www.kaggle.com/chasewillden/topstarredopensourceprojects


