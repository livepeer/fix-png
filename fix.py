#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from socketserver import ThreadingMixIn
import threading
from PIL import ImageFile, Image
import requests
import io
from urllib.parse import urlparse, parse_qs

hostName = "0.0.0.0"
serverPort = 80

class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
      ImageFile.LOAD_TRUNCATED_IMAGES = True

      # Parse the query string to get the value of the "image" parameter
      query_components = parse_qs(urlparse(self.path).query)
      image_url = query_components.get('image', [''])[0]
      
      # Check if the "image" parameter is present
      if not image_url:
          self.send_response(400)
          self.end_headers()
          self.wfile.write(b'Error: "image" parameter is required in the query string')
          return

      # Fetch the image data from the provided URL
      try:
          data = requests.get(image_url).content
          im = Image.open(io.BytesIO(data))
          im.load()
      except Exception as e:
          self.send_response(400)
          self.end_headers()
          self.wfile.write(f'Error: Failed to load image from URL: {e}'.encode())
          return
      
      # Save the image to a BytesIO object
      with io.BytesIO() as output:
          im.save(output, format="png")
          image_data = output.getvalue()

      # Send the image data through the socket
      self.send_response(200)
      self.send_header('Content-type', 'image/png')
      self.end_headers()
      self.wfile.write(image_data)
      return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

if __name__ == "__main__":
  webServer = ThreadedHTTPServer((hostName, serverPort), Handler)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
      webServer.serve_forever()
  except KeyboardInterrupt:
      pass

  webServer.server_close()
  print("Server stopped.")
