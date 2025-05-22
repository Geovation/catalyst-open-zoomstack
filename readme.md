# OS Open Zoomstack

This repository provides instructions for how to process [OS Open Zoomstack](https://www.ordnancesurvey.co.uk/products/os-open-zoomstack) data and host as static vector tiles. The data is available from Ordnance Survey under the Open Government Licence.

## Introduction

OS Open Zoomstack is a vector basemap of Great Britain. It is available as a set of vector tiles in the Mapbox Vector Tile format. The data is provided in a single `.mbtiles` file which can be downloaded from the Ordnance Survey data hub. That file is a SQLite database that contains the vector tiles.

Vector tiles are usually accessed in 'slippy' maps - web maps that allow you to pan and zoom. The tiles are requested by the client and rendered when they are required. This means that the client only has to request the tiles that are needed for the current view, which can make the map faster to load and more responsive.

The `.mbtiles` file could be used directly, and the tiles served up by a tile server. However, this requires backend processing to deliver the tiles. An alternative is that all the individual tiles can be extracted to a directory of static files. That makes them easy to host on a file server. If that storage can then be accessed on the web you can configure a URL to point to the data. No compute costs or server-side processing.

This project will provide sample code for:

1. Downloading and maintaining the OS Open Zoomstack data
2. Converting the mbtiles file to a directory of static files
3. Deploying the tiles to an online cloud service and providing a URL to access them

## GitHub hosting and restrictions

This project uses GitHub actions to create a fully automated process for updating OS vector tiles. However, GitHub is a free service (for public repositories) and we should be mindful of the resources we use.

GitHub have declared size limits. Firstly, files must be less than 100MB and ideally should be less than 50Mb. Pushing a file of 100MB or over will fail. That shouldn't matter in this situation we are only committing the code for processing the data.

Repository sizes are also limited. GitHub say a repository should be less than 5GB.

> We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended. Smaller repositories are faster to clone and easier to work with and maintain. If your repository excessively impacts our infrastructure, you might receive an email from GitHub Support asking you to take corrective action.
>
> [GitHub: Repository size limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#repository-size-limits)

So our example GitHub repository should only include files under 50Mb and we should avoid the repository becoming larger than 5GB.

There is no need to store the actual vector tiles or original `.mbtiles` file in this repository. The code for the respository is the relevant part, the tiles can be downloaded and processed on the fly.

We will be using GitHub actions to run a process to create the tiles and maintain these. GitHub actions are free for public repositories, and use [GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners) for running workflows. These have specific resources.

| Workflow type | Processor | Memory | Storage |
| ------------- | --------- | ------ | ------- |
| ubuntu-latest | 2         | 16GB   | 14GB    |

[Standard GitHub-hosted runners for public repositories](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for-public-repositories)

The biggest limitation here is probably storage space. As we need to download the data and generate tiles, we need to ensure there is enough storage available. 14GB should be enough!

## Third party hosting

We will provide examples of deploying the tiles to two different hosting facilities:

- AWS S3 bucket (coming soon)
- Azure storage

## Prerequisites

To run this project locally you will need:

- [Mapbox Tippecanoe](https://github.com/mapbox/tippecanoe)

When running on a GitHub runner this is installed within the GitHub action workflow.

## Download OS Open Zoomstack

OS Open Zoomstack is provided as a direct download link (via a redirect). The OS Data Hub download API could be used to check for new versions and download these but it is also straightforward to schedule the process to run periodically.

https://api.os.uk/downloads/v1/products/OpenZoomstack/downloads?area=GB&format=Vector+Tiles&subformat=%28MBTiles%29&redirect

## Convert mbtiles to vector tiles

The mbtiles file is a SQLite database. We can use `tile-join` which is part of the Mapbox tippecanoe tool to convert this to a directory of vector tiles. Another option would be to use `mbutil`.

```bash
tile-join --output-to-directory=tiles osopenzoomstack.mbtiles --force --no-tile-size-limit --minimum-zoom=0 --maximum-zoom=14
```

On a Macbook Pro M4 this process took around 5 minutes and the output directory was 2.63GB in size.

By default, tippecanoe (and tile-join) will create compressed vector tiles. This is a good thing - it makes the tiles smaller and faster to download.

The compressed tiles folder is around 2.63GB in size. There is an option to not compress the tiles.

```bash
tile-join --output-to-directory=tiles osopenzoomstack.mbtiles --force --no-tile-size-limit --minimum-zoom=0 --maximum-zoom=14 --no-tile-compression
```

This causes the tiles to be larger: without compression, the folder is 3.77GB in size.

Normally you would always use compression, however to serve them to a web client we would need to tell that client that they are compressed, so that the client knows to decompress them. This is set using the `Content-Encoding` header with a value of `gzip`. Depending on your hosting solution you may need to generate uncompressed tiles if you cannot set the response headers.

Compressed tiles could still be used with a host that doesn't support setting the `Content-Encoding` header, but this header would need to be set by a reverse proxy or CDN. For example, we could use [Cloudflare](https://www.cloudflare.com/en-gb/) to control a domain name and also to [modify the response headers](https://developers.cloudflare.com/rules/transform/response-header-modification/create-dashboard/). This would allow us to set the `Content-Encoding` header - it can also cache the tiles which would take load off the service hosting the tiles. Similar CDN solution exist on Azure, AWS, etc.

## Deploy

The GitHub actions workflow job includes steps to an Azure Storage Container. This could be done through an automatic deployment - for now we'll give instructions for how to set them up in the portal.

## Automation

OS Open Zoomstack is updated quarterly. This repository includes a GitHub action which will run every month to refresh the data. A future enhancement will be to run daily and use the download API to check for newer data.
