
# coding: utf-8

# # Logistic Regression with a Neural Network mindset
# 
# Welcome to the first (required) programming exercise of the deep learning specialization. In this notebook you will build your first image recognition algorithm. You will build a cat classifier that recognizes cats with 70% accuracy!
# 
# ![cats.png](attachment:cats.png)
# 
# As you keep learning new techniques you will increase it to 80+ % accuracy on cat vs. non-cat datasets. 
# 
# By completing this assignment you will:
# 
# - ** Work with logistic regression in a way that builds intuition relevant to neural networks.**
# 
# 
# - ** Learn how to minimize the cost function.**
# 
# 
# - ** Understand how derivatives of the cost are used to update parameters.**
# 
# Take your time to complete this assignment and make sure you get the expected outputs when working through the different exercises. 

# **Instructions:**
# - Do not use loops (for/while) in your code, unless the instructions explicitly ask you to do so.
# 
# **You will learn to:**
# - Build the general architecture of a learning algorithm, including:
#     - Initializing parameters
#     - Calculating the cost function and its gradient
#     - Using an optimization algorithm (gradient descent) 
# 
# - Gather all three functions above into a main model function, in the right order.

# **The main steps for building a Neural Network are:**
# 1. Define the model structure (such as number of input features) 
# 2. Initialize the model's parameters
# 3. Loop:
#     - Calculate current loss (forward propagation)
#     - Calculate current gradient (backward propagation)
#     - Update parameters (gradient descent)
# 
# We often build 1-3 separately and integrate them into one function we call `model()`.

# ### Steps:
# #### I. Import Packages
# #### II. Problem Statement
# #### III. Load the data
# #### IV. Reshape dataset
# #### V. Standardize/Normalize dataset
# #### VI. Architecture of the learning algorithm
# #### VII. Implement algorithm on training dataset
# #### VIII. Merge all functions into a model
# #### IX. Further analysis
# #### X. Test with your own image

# ## I. Import Packages

# First, let's run the cell below to import all the packages that you will need during this assignment. 
# - [numpy](www.numpy.org) is the fundamental package for scientific computing with Python.
# - [h5py](http://www.h5py.org) is a common package to interact with a dataset that is stored on an H5 file.
# - [matplotlib](http://matplotlib.org) is a famous library to plot graphs in Python.
# - [PIL](http://www.pythonware.com/products/pil/) and [scipy](https://www.scipy.org/) are used here to test your model with your own picture at the end.

# In[8]:


import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy
from PIL import Image # allows u to test with ur own pictures
from scipy import ndimage
from lr_utils import load_dataset

# lr_utils is a part of the deep learning course and is a utility to download the data sets

get_ipython().run_line_magic('matplotlib', 'inline')


# ## II. Overview of the Problem set 
# 
# **Problem Statement**: 
# 
# You are given a dataset ("data.h5") containing:
#     - a training set of m_train images labeled as cat (y=1) or non-cat (y=0)
#     - a test set of m_test images labeled as cat or non-cat
#     - each image is of shape (num_px, num_px, 3) where 3 is for the 3 channels (RGB). Thus, each image is square (height = num_px) and (width = num_px).
# 
# You will build a simple image-recognition algorithm that can correctly classify pictures as cat or non-cat.

# ## III. Load the dataset

# In[10]:


# Loading the data (cat/non-cat)
train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()


# We added "_orig" at the end of image datasets (train and test) because we are going to preprocess them. After preprocessing, we will end up with train_set_x and test_set_x (the labels train_set_y and test_set_y don't need any preprocessing).
# 
# Each line of your train_set_x_orig and test_set_x_orig is an array representing an image. You can visualize an example by running the following code. Feel free also to change the `index` value and re-run to see other images. 

# In[3]:


# Example of a picture
index = 7
plt.imshow(train_set_x_orig[index])
print ("y = " + str(train_set_y[:, index]) + ", it's a '" + 
       classes[np.squeeze(train_set_y[:, index])].decode("utf-8") +  "' picture.")


# __Many software bugs in deep learning come from having matrix/vector dimensions that don't fit. If you can keep your matrix/vector dimensions straight you will go a long way toward eliminating many bugs. __

# ### Explore the data
# 
# Find the values for:
#     - m_train (number of training examples)
#     - m_test (number of test examples)
#     - num_px (= height = width of a training image)
# Remember that `train_set_x_orig` is a numpy-array of shape (m_train, num_px, num_px, 3). For instance, you can access `m_train` by writing `train_set_x_orig.shape[0]`.

# This is quite common in computer vision the first dimension being the number of examples, the second and third provide the data of the examples. In the case of computer vision for example it is quite common to have a set of n images with shape (x,y). In this case your training set will be of the shape (n,x,y). The fourth dimension in your data is the number of channels (3, or RGB in this case).

# In[44]:


train_set_x_orig.shape


# In[45]:


print(train_set_x_orig)


# In[46]:


print (train_set_x_orig[208])


# In[47]:


print (train_set_x_orig[209]) #error b/c there're only 209 examples


# In[48]:


train_set_y.shape


# In[49]:


print(train_set_y)


# In[50]:


test_set_x_orig.shape


# In[51]:


test_set_y.shape


# In[31]:


# To help understand nested matrix
x = np.array(
    #1
        [
         [[[ 0, 1, 2],
           [ 3, 4, 5],
           [ 6, 7, 8],
           [ 9,10,11]],
           
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[21,31,41],
           [22,32,42],
           [23,33,43],
           [24,34,44]]],

    #2
         [[[10,11,12],
           [3, 4, 5],
           [6, 7, 8],
           [9,10,11]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[21,31,41],
           [22,32,42],
           [23,33,43],
           [24,34,44]]],
            
    #3
         [[[10,11,12],
           [3, 4, 5],
           [6, 7, 8],
           [9,10,11]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[21,31,41],
           [22,32,42],
           [23,33,43],
           [24,34,44]]],
            
    #4
         [[[10,11,12],
           [3, 4, 5],
           [6, 7, 8],
           [9,10,11]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[21,31,41],
           [22,32,42],
           [23,33,43],
           [24,34,44]]],
    
    #5
         [[[20,21,22],
           [3, 4, 5],
           [6, 7, 8],
           [9,10,11]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[11,21,31],
           [12,22,32],
           [13,23,33],
           [14,24,34]],
          
          [[21,31,41],
           [22,32,42],
           [23,33,43],
           [24,34,44]]]])
x.shape


# 5: 5 examples
# 
# 6: 6 matrix in each example
# 
# 4: row num is 4 in each matrix
# 
# 3: col num is 3 in each matrix

# In[32]:


x.shape[1]


# In[33]:


train_set_x_orig.shape[3]


# In[11]:


m_train = train_set_x_orig.shape[0] #b/c X is a nx by m matrix, [0]returns the length of the first row of the matrix
m_test = test_set_x_orig.shape[0]
num_px = train_set_x_orig.shape[1] #OR num_px = train_set_x_orig.shape[2] b/c height equals to width in this example

print ("Number of training examples: m_train = " + str(m_train))
print ("Number of testing examples: m_test = " + str(m_test))
print ("Height/Width of each image: num_px = " + str(num_px))
print ("Each image is of size: (" + str(num_px) + ", " + str(num_px) + ", 3)")
print ("train_set_x shape: " + str(train_set_x_orig.shape))
print ("train_set_y shape: " + str(train_set_y.shape))
print ("test_set_x shape: " + str(test_set_x_orig.shape))
print ("test_set_y shape: " + str(test_set_y.shape))


# Expected Output for m_train, m_test and num_px: 
# <table style="width:15%">
#   <tr>
#     <td>**m_train**</td>
#     <td> 209 </td> 
#   </tr>
#   
#   <tr>
#     <td>**m_test**</td>
#     <td> 50 </td> 
#   </tr>
#   
#   <tr>
#     <td>**num_px**</td>
#     <td> 64 </td> 
#   </tr>
#   
# </table>
# 

# For convenience, you should now reshape images of shape (num_px, num_px, 3) in a numpy-array of shape (num_px $*$ num_px $*$ 3, 1). After this, our training (and test) dataset is a numpy-array where each column represents a flattened image. There should be m_train (respectively m_test) columns.

# ## IV. Reshape the training and test data sets into matrix 
# 
# Reshape the training and test data sets so that images of size (num_px, num_px, 3) are flattened into single vectors of shape (num\_px $*$ num\_px $*$ 3, 1).
# 
# A trick when you want to flatten a matrix X of shape (a,b,c,d) to a matrix X_flatten of shape (b$*$c$*$d, a) is to use: 
# ```python
# X_flatten = X.reshape(X.shape[0], -1).T      # X.T is the transpose of X
# # Or
# X_flatten = X.reshape(12288, X.shape[0])
# ```

# ![reshape.PNG](attachment:reshape.PNG)

# In[ ]:


# Reshape the training and test examples
train_set_x_flatten = train_set_x_orig.reshape((train_set_x_orig.shape[1]*train_set_x_orig.shape[2]*train_set_x_orig.shape[3],1))
test_set_x_flatten = test_set_x_orig.reshape((test_set_x_orig.shape[1]*test_set_x_orig.shape[2]*test_set_x_orig.shape[3],1))

print ("train_set_x_flatten shape: " + str(train_set_x_flatten.shape))
print ("train_set_y shape: " + str(train_set_y.shape))
print ("test_set_x_flatten shape: " + str(test_set_x_flatten.shape))
print ("test_set_y shape: " + str(test_set_y.shape))
print ("sanity check after reshaping: " + str(train_set_x_flatten[0:5,0]))


# **Q: Why not working? **
# 
# **S: B/c here train_set_x_orig.shape[1] is the num of the first training example rather than the length/width/num of color img**

# In[12]:


# Reshape the training and test examples
train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0],-1).T 
# -1 here means the unspecified value, in this case is length*width*3, which is 64*64*3=12288
test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0],-1).T 

print ("train_set_x_flatten shape: " + str(train_set_x_flatten.shape))
print ("train_set_y shape: " + str(train_set_y.shape))
print ("test_set_x_flatten shape: " + str(test_set_x_flatten.shape))
print ("test_set_y shape: " + str(test_set_y.shape))
print ("sanity check after reshaping: " + str(train_set_x_flatten[0:5,0]))


# **Expected Output**: 
# 
# <table style="width:35%">
#   <tr>
#     <td>**train_set_x_flatten shape**</td>
#     <td> (12288, 209)</td> 
#   </tr>
#   <tr>
#     <td>**train_set_y shape**</td>
#     <td>(1, 209)</td> 
#   </tr>
#   <tr>
#     <td>**test_set_x_flatten shape**</td>
#     <td>(12288, 50)</td> 
#   </tr>
#   <tr>
#     <td>**test_set_y shape**</td>
#     <td>(1, 50)</td> 
#   </tr>
#   <tr>
#   <td>**sanity check after reshaping**</td>
#   <td>[17 31 56 22 33]</td> 
#   </tr>
# </table>

# ## V. Standardize/Normalize the training matrix

# To represent color images, the red, green and blue channels (RGB) must be specified for each pixel, and so the pixel value is actually a vector of three numbers ranging from 0 to 255.
# 
# One common preprocessing step in machine learning is to center and standardize your dataset, meaning that you substract the mean of the whole numpy array from each example, and then divide each example by the standard deviation of the whole numpy array. But for picture datasets, it is simpler and more convenient and works almost as well to just divide every row of the dataset by 255 (the maximum value of a pixel channel).
# 
# <!-- During the training of your model, you're going to multiply weights and add biases to some initial inputs in order to observe neuron activations. Then you backpropogate with the gradients to train the model. But, it is extremely important for each feature to have a similar range such that our gradients don't explode. You will see that more in detail later in the lectures. !--> 

# In[13]:


train_set_x = train_set_x_flatten/255.
test_set_x = test_set_x_flatten/255.


# ### General way of standardization

# In[34]:


train_set_norm = np.linalg.norm(train_set_x_flatten, axis=1, keepdims=True) #axis=1 means normalize by rows
train_set_normalized = train_set_x_flatten / train_set_norm


# In[35]:


#check the answer
print(train_set_norm)
print(train_set_normalized)


# ## VI. Architecture of the learning algorithm
# 
# Building a Logistic Regression, using a Neural Network mindset to design a simple algorithm to distinguish cat images from non-cat images.
# 
# <img src="images/LogReg_kiank.png" style="width:650px;height:400px;">
# 
# **Mathematical expression of the algorithm**:
# 
# For one example $x^{(i)}$:
# $$z^{(i)} = w^T x^{(i)} + b \tag{1}$$
# $$\hat{y}^{(i)} = a^{(i)} = sigmoid(z^{(i)})\tag{2}$$ 
# $$ \mathcal{L}(a^{(i)}, y^{(i)}) =  - y^{(i)}  \log(a^{(i)}) - (1-y^{(i)} )  \log(1-a^{(i)})\tag{3}$$
# 
# The cost is then computed by summing over all training examples:
# $$ J = \frac{1}{m} \sum_{i=1}^m \mathcal{L}(a^{(i)}, y^{(i)})\tag{6}$$

# <font color='red'>
# **Key steps**:
# - Initialize the parameters of the model
# - Learn the parameters for the model by minimizing the cost  
# - Use the learned parameters to make predictions (on the test set)
# - Analyse the results and conclude

# ## VII. Implement algorithm on training dataset

# ### 1 - Helper functions
# 
# **Using your code from "Python Basics", implement `sigmoid()`. As you've seen in the figure above, you need to compute $sigmoid( w^T x + b) = \frac{1}{1 + e^{-(w^T x + b)}}$ to make predictions. Use np.exp().: **

# In[14]:


# GRADED FUNCTION: sigmoid

def sigmoid(z): # Compute the sigmoid of z

    s = 1/(1+np.exp(-z))
    
    return s


# In[36]:


print ("sigmoid([0, 2]) = " + str(sigmoid(np.array([0,2]))))


# Expected Output: 
# 
# <table>
#   <tr>
#     <td>**sigmoid([0, 2])**</td>
#     <td> [ 0.5         0.88079708]</td> 
#   </tr>
# </table>

# ### 2 - Initializing parameters
# 
# **Implement parameter initialization in the cell below. You have to initialize w as a vector of zeros. If you don't know what numpy function to use, look up np.zeros() in the Numpy library's documentation.**

# In[ ]:


get_ipython().run_line_magic('pinfo', 'np.zeros')


# In[15]:


# GRADED FUNCTION: initialize_with_zeros

def initialize_with_zeros(dim): #creates a vector of zeros of shape (dim, 1) for w and initializes b to 0.
    #dim -- size of the w vector we want (or number of parameters in this case)
    
    w = np.zeros([dim,1])
    b = 0

    assert(w.shape == (dim, 1))
    assert(isinstance(b, float) or isinstance(b, int))
    
    return w, b #w -- initialized vector of shape (dim, 1), b -- initialized scalar (corresponds to the bias)


# In[37]:


#Test
dim = 2
w, b = initialize_with_zeros(dim)
print ("w = " + str(w))
print ("b = " + str(b))


# Expected Output: 
# 
# 
# <table style="width:15%">
#     <tr>
#         <td>  ** w **  </td>
#         <td> [[ 0.]
#  [ 0.]] </td>
#     </tr>
#     <tr>
#         <td>  ** b **  </td>
#         <td> 0 </td>
#     </tr>
# </table>
# 
# For image inputs, w will be of shape (num_px $\times$ num_px $\times$ 3, 1).

# ### 3 - Forward and Backward propagation
# 
# Now that your parameters are initialized, you can do the "forward" and "backward" propagation steps for learning the parameters.
# 

# #### Forward Propagation:
# - You get X
# - You compute $A = \sigma(w^T X + b) = (a^{(1)}, a^{(2)}, ..., a^{(m-1)}, a^{(m)})$
# - You calculate the cost function: $J = -\frac{1}{m}\sum_{i=1}^{m}y^{(i)}\log(a^{(i)})+(1-y^{(i)})\log(1-a^{(i)})$
# 
# Here are the two formulas you will be using: 
# 
# $$ \frac{\partial J}{\partial w} = \frac{1}{m}X(A-Y)^T\tag{7}$$
# $$ \frac{\partial J}{\partial b} = \frac{1}{m} \sum_{i=1}^m (a^{(i)}-y^{(i)})\tag{8}$$

# __squeeze function__

# In[38]:


x = np.array([[[0], [1], [2]]])
x


# In[39]:


x=np.squeeze(x)
x


# **Notice the difference between np.dot() and * :**
# 
# __"np.dot(a,b)" performs a matrix multiplication on a and b, whereas "a*b" performs an element-wise multiplication.__

# In[16]:


# GRADED FUNCTION: propagate to compute the cost function and its gradient

def propagate(w, b, X, Y):
    """
    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of size (num_px * num_px * 3, m)
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat) of size (1, number of examples)

    Return:
    cost -- negative log-likelihood cost for logistic regression
    dw -- gradient of the loss with respect to w, thus same shape as w
    db -- gradient of the loss with respect to b, thus same shape as b
    """
    
    m = X.shape[1] # for data after reshape
    
    # FORWARD PROPAGATION (FROM X TO COST)
    A = sigmoid(np.dot(w.T,X)+b) # compute y hat
    cost = -1/m* (np.dot(Y,np.log(A).T) + np.dot((1-Y),np.log(1-A).T)) # compute cost
    # numpy.sum https://www.geeksforgeeks.org/numpy-sum-in-python/
    
    # BACKWARD PROPAGATION (TO FIND GRAD)
    dw = 1/m * np.dot(X,(A-Y).T)
    db = 1/m * np.sum(A-Y)

    '''
    statement is used to check types, values of argument and the output of the function, 
    also is used as debugging tool as it halts the program at the point where an error occurs.
    '''
    assert(dw.shape == w.shape) 
    assert(db.dtype == float)
    cost = np.squeeze(cost)
    assert(cost.shape == ())
    
    grads = {"dw": dw,
             "db": db}
    
    return grads, cost


# In[41]:


#Test:
w, b, X, Y = np.array([[1.],[2.]]), 2., np.array([[1.,2.,-1.],[3.,4.,-3.2]]), np.array([[1,0,1]])
grads, cost = propagate(w, b, X, Y)
print ("dw = " + str(grads["dw"]))
print ("db = " + str(grads["db"]))
print ("cost = " + str(cost))


# Expected Output:
# 
# <table style="width:50%">
#     <tr>
#         <td>  ** dw **  </td>
#       <td> [[ 0.99845601]
#      [ 2.39507239]]</td>
#     </tr>
#     <tr>
#         <td>  ** db **  </td>
#         <td> 0.00145557813678 </td>
#     </tr>
#     <tr>
#         <td>  ** cost **  </td>
#         <td> 5.801545319394553 </td>
#     </tr>
# 
# </table>

# ### 4 - Optimization
# - You have initialized your parameters.
# - You are also able to compute a cost function and its gradient.
# - Now, you want to __update the parameters using gradient descent__.

# **Write down the optimization function. The goal is to learn $w$ and $b$ by minimizing the cost function $J$. For a parameter $\theta$, the update rule is $ \theta = \theta - \alpha \text{ } d\theta$, where $\alpha$ is the learning rate.**

# In[17]:


# GRADED FUNCTION: optimize

def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost = False):
    """
    This function optimizes w and b by running a gradient descent algorithm
    
    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of shape (num_px * num_px * 3, number of examples)
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat), of shape (1, number of examples)
    num_iterations -- number of iterations of the optimization loop
    learning_rate -- learning rate of the gradient descent update rule
    print_cost -- True to print the loss every 100 steps
    
    Returns:
    params -- dictionary containing the weights w and bias b
    grads -- dictionary containing the gradients of the weights and bias with respect to the cost function
    costs -- list of all the costs computed during the optimization, this will be used to plot the learning curve.
    
    Steps:
        1) Use propagate() to calculate the cost and the gradient for the current parameters.
        2) Update the parameters using gradient descent rule for w and b.
    """
    
    costs = [] # as a list
    
    for i in range(num_iterations):
        
        # Cost and gradient calculation
        grads, cost = propagate(w,b,X,Y)
        
        # Retrieve derivatives from dictionary grads
        dw = grads["dw"] 
        db = grads["db"]
        
        # update w & b
        w -= learning_rate*dw
        b -= learning_rate*db
        
        # Record the costs every 100 training iterations
        if i % 100 == 0: # the % operator returns the remainder of the division
            costs.append(cost)
        
        # Print the cost every 100 training iterations
        if print_cost and i % 100 == 0: 
            print ("Cost after iteration %i: %f" %(i, cost))
    
    params = {"w": w,
              "b": b}
    
    grads = {"dw": dw,
             "db": db}
    
    return params, grads, costs


# In[42]:


#Test:
params, grads, costs = optimize(w, b, X, Y, num_iterations= 100, learning_rate = 0.009, print_cost = False)

print ("w = " + str(params["w"]))
print ("b = " + str(params["b"]))
print ("dw = " + str(grads["dw"]))
print ("db = " + str(grads["db"]))


# Expected Output: 
# 
# <table style="width:40%">
#     <tr>
#        <td> **w** </td>
#        <td>[[ 0.19033591]
#  [ 0.12259159]] </td>
#     </tr>
#     
#     <tr>
#        <td> **b** </td>
#        <td> 1.92535983008 </td>
#     </tr>
#     <tr>
#        <td> **dw** </td>
#        <td> [[ 0.67752042]
#  [ 1.41625495]] </td>
#     </tr>
#     <tr>
#        <td> **db** </td>
#        <td> 0.219194504541 </td>
#     </tr>
# 
# </table>

# ### 5 - Prediction function

# The previous function will output the learned w and b. We are able to use w and b to predict the labels for a dataset X. Implement the `predict()` function. There are two steps to computing predictions:
# 
# 1. Calculate $\hat{Y} = A = \sigma(w^T X + b)$
# 
# 2. Convert the entries of a into 0 (if activation <= 0.5) or 1 (if activation > 0.5), stores the predictions in a vector `Y_prediction`. If you wish, you can use an `if`/`else` statement in a `for` loop (though there is also a way to vectorize this). 

# In[18]:


# GRADED FUNCTION: predict

def predict(w, b, X):
    '''
    Predict whether the label is 0 or 1 using learned logistic regression parameters (w, b)
    
    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of size (num_px * num_px * 3, number of examples)
    
    Returns:
    Y_prediction -- a numpy array (vector) containing all predictions (0/1) for the training examples in X
    '''
    # Initialize parameters
    m = X.shape[1] # columns of X
    Y_prediction = np.zeros((1,m))
    w = w.reshape(X.shape[0], 1) # rows of X
    
    # Compute vector "A" predicting the probabilities of a cat being present in the picture
    A = sigmoid(np.dot(w.T,X)+b)
    
    assert(A.shape == (1, m))
    
    for i in range(A.shape[1]): # the num of testing examples
        # Convert probabilities A[0,i] to actual predictions p[0,i]
        if A[0,i] <= 0.5: # instead of A[0][i]!!!Syntax!
            Y_prediction[0,i] = 0
        else:
            Y_prediction[0,i] = 1
        # Use the pass statement to construct a body that does nothing.
    
    assert(Y_prediction.shape == (1, m))
    
    return Y_prediction


# In[43]:


#Test:
w = np.array([[0.1124579],[0.23106775]])
b = -0.3
X = np.array([[1.,-1.1,-3.2],[1.2,2.,0.1]])
print ("predictions = " + str(predict(w, b, X)))


# **Expected Output**: 
# 
# <table style="width:30%">
#     <tr>
#          <td>
#              **predictions**
#          </td>
#           <td>
#             [[ 1.  1.  0.]]
#          </td>  
#    </tr>
# 
# </table>
# 

# ## VIII. Merge all functions into a model
# 
# You will now see how the overall model is structured by putting together all the building blocks (functions implemented in the previous parts) together, in the right order.
# 
# **Implement the model function using the following notation:**
#     - Y_prediction_test for your predictions on the test set
#     - Y_prediction_train for your predictions on the train set
#     - w, costs, grads for the outputs of optimize()

# In[28]:


# GRADED FUNCTION: model

def model(X_train, Y_train, X_test, Y_test, num_iterations = 2000, learning_rate = 0.5, print_cost = False):
    """
    Builds the logistic regression model by calling the function that are implemented previously
    
    Arguments:
    X_train -- training set represented by a numpy array of shape (num_px * num_px * 3, m_train)
    Y_train -- training labels represented by a numpy array (vector) of shape (1, m_train)
    X_test -- test set represented by a numpy array of shape (num_px * num_px * 3, m_test)
    Y_test -- test labels represented by a numpy array (vector) of shape (1, m_test)
    num_iterations -- hyperparameter representing the number of iterations to optimize the parameters
    learning_rate -- hyperparameter representing the learning rate used in the update rule of optimize()
    print_cost -- Set to true to print the cost every 100 iterations
    
    Returns:
    d -- dictionary containing information about the model.
    """
        
    # initialize parameters with zeros 
    dim = X_train.shape[0]
    w, b = initialize_with_zeros(dim)

    # Gradient descent
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost = print_cost)
    
    # Retrieve parameters w and b from dictionary "parameters"
    w = parameters["w"]
    b = parameters["b"]
    
    # Predict test/train set examples
    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train)

    # Print train/test Errors
    print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))
    print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))

    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}
    
    return d


# __train your model__

# In[29]:


d = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 2000, learning_rate = 0.005, print_cost = True)


# Expected Output: 
# 
# <table style="width:40%"> 
# 
#     <tr>
#         <td> **Cost after iteration 0 **  </td> 
#         <td> 0.693147 </td>
#     </tr>
#       <tr>
#         <td> <center> $\vdots$ </center> </td> 
#         <td> <center> $\vdots$ </center> </td> 
#     </tr>  
#     <tr>
#         <td> **Train Accuracy**  </td> 
#         <td> 99.04306220095694 % </td>
#     </tr>
# 
#     <tr>
#         <td>**Test Accuracy** </td> 
#         <td> 70.0 % </td>
#     </tr>
# </table> 
# 
# 
# 

# Training accuracy is close to 100%. This is a good sanity check that the model is working and has high enough capacity to fit the training data. Test error is 68%. It is actually not bad for this simple model, given the small dataset we used and that logistic regression is a linear classifier. 
# 
# Also, we can see that the model is clearly overfitting the training data. Later in this specialization you will learn how to **reduce overfitting**, for example by using **regularization**. Using the code below (and changing the `index` variable) you can look at predictions on pictures of the test set.

# In[21]:


# Example of a picture
index = 5
plt.imshow(test_set_x_orig[index])
print ("y = " + str(test_set_y[:, index]) + ", it's a '" + 
       classes[np.squeeze(test_set_y[0, index])].decode("utf-8") +  "' picture.")


# __plot the cost function and the gradients__

# In[22]:


# Plot learning curve (with costs)
costs = np.squeeze(d['costs'])
plt.plot(costs)
plt.ylabel('cost')
plt.xlabel('iterations (per hundreds)')
plt.title("Learning rate =" + str(d["learning_rate"]))
plt.show()


# **Interpretation**:
# You can see the cost decreasing. It shows that the parameters are being learned. However, you see that you could train the model even more on the training set. Try to increase the number of iterations in the cell above and rerun the cells. You might see that the training set accuracy goes up, but the test set accuracy goes down. This is called overfitting. 

# ## IX. Further analysis
# 
# Analyze further to examine possible choices for the learning rate $\alpha$. 

# #### Choice of learning rate ####
# 
# **Reminder**:
# In order for Gradient Descent to work you must choose the learning rate wisely. The learning rate $\alpha$  determines how rapidly we update the parameters. If the learning rate is too large we may "overshoot" the optimal value. Similarly, if it is too small we will need too many iterations to converge to the best values. That's why it is crucial to use a well-tuned learning rate.
# 
# Let's compare the learning curve of our model with several choices of learning rates. Run the cell below. This should take about 1 minute. Feel free also to try different values than the three we have initialized the `learning_rates` variable to contain, and see what happens. 

# In[30]:


learning_rates = [0.01, 0.001, 0.0001]
models = {}
for i in learning_rates:
    print ("learning rate is: " + str(i))
    models[str(i)] = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 1500, learning_rate = i, print_cost = False)
    print ('\n' + "-------------------------------------------------------" + '\n')

for i in learning_rates:
    plt.plot(np.squeeze(models[str(i)]["costs"]), label= str(models[str(i)]["learning_rate"]))

plt.ylabel('cost')
plt.xlabel('iterations (hundreds)')

legend = plt.legend(loc='upper center', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.show()


# **Interpretation**: 
# - Different learning rates give different costs and thus different predictions results.
# - If the learning rate is too large (0.01), the cost may oscillate up and down. It may even diverge (though in this example, using 0.01 still eventually ends up at a good value for the cost). 
# - A lower cost doesn't mean a better model. You have to check if there is possibly overfitting. It happens when the training accuracy is a lot higher than the test accuracy.
# - In deep learning, we usually recommend that you: 
#     - Choose the learning rate that better minimizes the cost function.
#     - If your model overfits, use other techniques to reduce overfitting. (We'll talk about this in later videos.) 
# 

# ## X. Test with your own image
# 
# You can use your own image and see the output of your model. To do that:
#     1. Click on "File" in the upper bar of this notebook, then click "Open" to go on your Coursera Hub.
#     2. Add your image to this Jupyter Notebook's directory, in the "images" folder
#     3. Change your image's name in the following code
#     4. Run the code and check if the algorithm is right (1 = cat, 0 = non-cat)!

# In[25]:


## START CODE HERE ## (PUT YOUR IMAGE NAME) 
my_image = "my_image4.jpg"   # change this to the name of your image file 
## END CODE HERE ##

# We preprocess the image to fit your algorithm.
fname = "images/" + my_image
image = np.array(ndimage.imread(fname, flatten=False))
my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
my_image = my_image/255
my_predicted_image = predict(d["w"], d["b"], my_image)

plt.imshow(image)
print("y = " + str(np.squeeze(my_predicted_image)) + ", your algorithm predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")


# Possible ways to improve testing rate:
# - scale the pics
# - more training data

# <font color='blue'>
# **What to remember from this assignment:**
# 1. Preprocessing the dataset is important.
# 2. You implemented each function separately: initialize(), propagate(), optimize(). Then you built a model().
# 3. Tuning the learning rate (which is an example of a "hyperparameter") can make a big difference to the algorithm. You will see more examples of this later in this course!

# Finally, if you'd like, we invite you to try different things on this Notebook. Make sure you submit before trying anything. Once you submit, things you can play with include:
#     - Play with the learning rate and the number of iterations
#     - Try different initialization methods and compare the results
#     - Test other preprocessings (center the data, or divide each row by its standard deviation)

# Bibliography
# - https://datascience-enthusiast.com/DL/Logistic-Regression-with-a-Neural-Network-mindset.html (useful reference)
# - http://www.wildml.com/2015/09/implementing-a-neural-network-from-scratch/
# - https://stats.stackexchange.com/questions/211436/why-do-we-normalize-images-by-subtracting-the-datasets-image-mean-and-not-the-c
