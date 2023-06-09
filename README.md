# ForestFireDemo


This is the demo repo for the Forest Fire Project.
In the Scripts directory there are script regarding each node connecting to the server, the server script and the html and css files for that.
Each node script will use a pretrained model to predict the probability of a random image in the dataset directory to present fire in it.
The outcome of the prediction is sent in a message using protobuffer to the server. The message is composed by two fields: id and data.
The id will be used to identify which node is sending the message, while the data will be used to perform an hardvote in the server.

The server will be hosted on 127.0.0.1:5000, that will show the dict with the data set by the nodes.
The webpage with all the informations will be hosted on 127.0.0.1:5000/view.

In the end the server hosted in flask will provide informations about the whole system and the decision made after the vote.
An example of the demo can be seen below:

![Demo](https://github.com/Immaioz/ForestFireDemo/assets/49716352/a239d09d-43d4-44b8-a481-90d1d401db32)
