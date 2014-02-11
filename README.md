ihulk
=====

Advanced Web Server DoS Tool/Web Stress Tool

useage:
python ihulk.py [threads] url

Some Techniques:
1. Obfuscation of Source Client – this is done by using a list of known User Agents, and for every request that is constructed, the User Agent is a random value out of the useragent list
2. Reference Forgery – the referer that points at the request is obfuscated and points into either the host itself or some major prelisted websites.
3. Stickiness – using some standard Http command to try and ask the server to maintain open connections by using Keep-Alive with variable time window
4. no-cache – this is a given, but by asking the HTTP server for no-cache , a server that is not behind a dedicated caching service will present a unique page.
5. Unique Transformation of URL – to eliminate caching and other optimization tools, I crafted custom parameter names and values and they are randomized and attached to each request, rendering it to be Unique, causing the server to process the response on each event.

