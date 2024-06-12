# serverless function

from http.server import BaseHTTPRequestHandler
import requests
from urllib import parse
class handler(BaseHTTPRequestHandler):

    def do_GET(self):
      
      
      base_url = f"https://opentdb.com/api.php?"
      s = self.path
      url_component = parse.urlsplit(s)
      query_string_list = parse.parse_qsl(url_component.query)
      my_dic = dict(query_string_list)
     
      
      if 'category' in my_dic:
        category_id = my_dic['category']
        if int(category_id) > 32 or int(category_id) < 9:
          self.send_response(400)
          self.send_header('Content-type', 'text/plain')
          self.end_headers()
          msg = 'error: enter category number between 9 and 32'
          self.wfile.write(msg.encode())
          return
        base_url += f"amount=10&category={category_id}"
        req = requests.get(base_url)
        data = req.json()
        # questions = data['results']
        questions = (data['results'])
        display = f"{self.get_category_name(category_id)} Category\n\n"
        for question in questions:
          display += f"Question: {question['question']}\nAnswer: {question['correct_answer']}\n\n"
          
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        msg = display
        self.wfile.write(msg.encode())
        return
          
        
        
        
      elif 'amount' in my_dic:
        amount = my_dic['amount']
        if int(amount) > 50:
          self.send_response(400)
          self.send_header('Content-type', 'text/plain')
          self.end_headers()
          msg = 'error: maximum questions is 50'
          self.wfile.write(msg.encode())
          return
        print(type(amount))
        base_url += f"amount={amount}"
        
        req = requests.get(base_url)
        data = req.json()
        questions = data['results']
   
        display = ''
        for question in questions:
          display += f"Question: {question['question']}\nAnswer: {question['correct_answer']}\n\n"
          
          
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        msg = display
        self.wfile.write(msg.encode())
        return
      else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            msg = "error:\nenter the path as following:\nhttps://questions-competition-git-serverless-lab-anasknbars-projects.vercel.app/api/questions?amount=3 or\nhttps://questions-competition-git-serverless-lab-anasknbars-projects.vercel.app/api/questions?category=21"
            self.wfile.write(msg.encode())
            return
      
    
     
        
     
      
      
    def get_category_name(self,category_id):
      base_url = "https://opentdb.com/api_category.php"
        
      req = requests.get(base_url)
      data = req.json()
      data = data['trivia_categories']
      
      for item in data:
        if item['id'] == int(category_id):
          return(item['name']) 
      
      