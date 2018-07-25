# mesos-log-scraper
Almost everyone who has used Orchestrator knows the pain in monitoring running mesos container logs, primarily because 
1. You need to follow 7-8 steps to land to the mesos stdout logs page
2. You will have to change the proxy accordingly 
3. Download a file of 256 MB size, just to analyze a log message of 1 KB, or
4. Click on stdout to monitor 'running logs' via stdout. You end up cursing and try to make sense out of the infinitely scrolling logs in mesos UI. Most of the times these logs are gone before even you catch a glimpse of them
5. The whole process takes around 5-10 minutes for each request (it takes even longer if your internet connection is slow)

In short, we had always missed Opsworks for this particular reason. Opsworks provides superior control in monitoring the system and real-time logs via console/terminal, it is pretty easy to drill down to the request which caused some Exception (using Unix commands). But the same does not apply for Orchestrator because of multiple reasons.

This frustration lead me to build a tool which now helps us access mesos container logs via Terminal, just like Opsworks. Yes, you heard it right. All you have to do is run the following commands
1. Login to the Jump server where this application is accessible 
2. Export your application's mesos log URL to local env variable. 
	- To get the mesos container logs URL, all you have to do is on mesos stdout HTML page, click on inspect element and get the URL from the Network tab. 
	- This is just a one-time activity per terminal session. 
	- For Example, the URL can be exported to local env variable with the following command 
export MESOS_URL="<Your mesos URL here>"
3. Then finally hit the following command to check the logs via Terminal
	- python3 ./mesos_logs.py 2>&1

And that's it. You have all the running logs in front of you, on the terminal. These logs will stay there on your terminal, till the time you close it. You won't need any special permissions/access to run the above.

You can then use any Unix/Linux command to drill down to the logs of your interest. For instance, suppose you want to monitor exceptions in your application, then the command in step 4 will be as follows 
python3 ./mesos_logs.py 2>&1 | grep Exception

Another point to note is, the above can be used to check logs on any environment. You just need to run the commands from the corresponding jump servers. 