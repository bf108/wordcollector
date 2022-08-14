# URL Aggregated Word Count App

This is a simple one page Flask Application which receives user input of a valid URL which doesn't require login. 
The application will then return a list of the words which appear on that page. 
Words will be presented in descening order of appearance.

### A Live Demo of APP Hosted on Heroku [HERE](https://wordcountappbf.herokuapp.com/)

## User Input
Users can type in urls into the search bar and search by clicking "Collect Words" button below

User will be given brief summary of the error message from the failed request.

## Returned Word Format
Things to note about returned words:
- Any leading or trailing whitespace will be removed from words
- Leading or trailing punctuation on words will be removed
- All words will be coverted into lower case
- Numbers will also be stripped out.

  Some examples of what behaviour to expect:
  * Goal!!!! --> goal
  * 4Life! --> life
  
## Underlying API to collect Words
This is a standalone package wordcollect/textgrab/textgrab.py

1. This preprocesses the input url:
  - Temoves whitespace, lowercases all text, incluedes schema (https://) if missing etc
  
2. Then it makes use of two key python libraries to make the request and parse the response:
  - [requests](https://requests.readthedocs.io/en/latest/)
  - [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  
3. The raw text is then split into individual words which are normalized

4. Aggreated count of words found is then returned descending order

## Running App Locally
- Simply clone repo
- Assumes you have python3.9 and pip installed
- Create a python virtualenv with following command in terminal:

```
python3 -m venv venv
pip3 install -r requirements.txt
#While in route dir
python app.py
```

## Tests

There are a set of unit tests in textgrab/tests/textgrab_test.py

These check for the formatting of URL and formatting of the response.

Run tests by calling:

From project route dir
```
python3 -m pytest
```


## Docker
Dockerfile provides a set of instruction for how to build the Docker Image. To create equivalent Docker image: 

- Ensure docker is installed
- From project route dir call 
- Run following commands in bash terminal
  ```
  #Creating docker image
  docker build -t <PICK_ANY_NAME_FOR_IMAGE> .
  
  #Creating instance of the image
  #In the Flask application, we have specified to run on PORT=8000. Here we are ensuring that we expose PORT 8000 on the Docker Image for the 
  docker run -p 8000:8000 <NAME_OF_IMAGE_ABOVE>
  
  ```

## Heroku

If intending to deploy on Heroku then you will also require the **Procfile**

For support deploying on Heroku follow this excellent [guide](https://dev.to/ejach/how-to-deploy-a-python-flask-app-on-heroku-using-docker-mpc)


