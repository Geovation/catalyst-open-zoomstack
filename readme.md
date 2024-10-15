# OS Open Zoomstack

This is a simple example of how to process OS Open Zoomstack data and host as static vector tiles. The data is available from the Ordnance Survey under the Open Government Licence.



GitHub have declared size limits. Firstly, files must be less than 100MB. Even trying to push a file of 100MB will fail. That doesn't really matter in this example - vector tiles are very small despite there being a lot of them.

However, a repository should ideally be less than 1GB and should be less than 5GB. Going over those limits may result in contact from GitHub.

> 

The extracted folder of Open Zoomstack data is 


We should be careful and sensitive though. GitHub is a free service and we should be mindful of the resources we use. If you're going to be serving a lot of data for your own organisational project, you should consider hosting your own static tiles service. It is relatively easy to do and there are many options available.

One problem with hosting vector tiles on GitHub is the commit history. GitHub is a version control system. Each change is stored and the entire history is available. This is great for code, but not so great for files that are effectively output.

To be mindful of this we will push the output to a separate, clean branch. On every refresh we will force a fresh and clean history for that branch. This will keep the repository size down and make it easier to manage.


## Process

What's the end to end process?

1. Download OS Open Zoomstack mbtiles file using the [OS Data Hub](https://osdatahub.os.uk/) and the [OS Open Zoomstack](https://osdatahub.os.uk/downloads/open/zoomstack) product. This can be automated using the. We can set this up to run on a schedule to keep the data up to date. If a new version of the data is available, we can download it and process the data.
2. 

## End result

- Repository size: 
- Update frequency
- Vector tiles hosted on GitHub Pages


Lovely stuff

## How to use

