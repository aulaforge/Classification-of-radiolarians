mobilenet-on-radiolarians : MobileNet applied on the radiolarian data set. It trains the model with our images and shows the result with a confusion matrix.

code prediction by the trained model : Once the model has been trained, you can save its parameters. In this notebook, we use these parameters to predict the classification of an image by the network, without doing a training, which has been done already.

test conversion mobilenet nengo dl : I tried to convert the mobilenet network into Nengo, to turn it into a spiking network. Unfortunately, it wasn't successful.

The xlsx document contains the stats of mobilenet trained on the radiolarians, tested on 10 runs.
