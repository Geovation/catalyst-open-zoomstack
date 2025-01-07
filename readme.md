# OS Open Zoomstack

This is an example of how to process OS Open Zoomstack data and host as static vector tiles. The data is available from Ordnance Survey under the Open Government Licence.

## Introduction

OS Open Zoomstack is a vector basemap of Great Britain. It is available as a set of vector tiles in the Mapbox Vector Tile format. The data is provided in a single mbtiles file which can be downloaded from the Ordnance Survey website. An mbtiles file is a SQLite database that contains the vector tiles.

Vector tiles are usually accessed in 'slippy' maps - web maps that allow you to pan and zoom. The tiles are requested by the client and rendered on the client side. This means that the client can request only the tiles that are needed for the current view, which can make the map faster to load and more responsive.

The `mbtiles` file can be served up by a tile server, but can also be converted to a simple directory of static files. That makes it easy to host on a static file server where only the data storage is required, and a URL to point to the data. No compute costs or server-side processing is required.

This project will demonstrate:

1. Downloading and maintaining the OS Open Zoomstack data
2. Converting the mbtiles file to a directory of static files
3. Hosting the vector tiles and providing a URL to access them

## GitHub hosting and restrictions

This project uses GitHub actions and GitHub pages to create a fully automated process for updating and hosting OS vector tiles. However, GitHub is a free service (to public repositories) and we should be mindful of the resources we use.

GitHub have declared size limits. Firstly, files must be less than 100MB and ideally should be less than 50Mb. Pushing a file of 100MB or over will fail. That shouldn't matter in this situation - vector tiles are small, despite there being a lot of them.

Rerpository sizes are also limited. GitHub say a repository should be less than 5GB.

> We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended. Smaller repositories are faster to clone and easier to work with and maintain. If your repository excessively impacts our infrastructure, you might receive an email from GitHub Support asking you to take corrective action.
>
> [GitHub: Repository size limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#repository-size-limits)

So our example GitHub repository should only include files under 50Mb and we should avoid the repository becoming larger than 5GB. It is worth being wary of commit history. GitHub is a version control system. Each change is stored and the entire history of file changes is available. This is great for code, but when a significant number of files are created, and updated, this history can accumulate quickly, even after files are deleted. To be mindful of this we will push the output tiles to a separate, clean branch. On every refresh we will force a fresh and clean history for that branch. This will keep the repository size down and make it easier to manage.

If you're going to be serving a lot of data for your own organisational project, you should host your own static tile service. It is relatively easy to do and there are many options available. This repostory could easily be used to help you in creating the vector tiles and then you could host them yourself.

We will be using GitHub actions to perform maintenance and run processes to create the tiles. GitHub actions are free for public repositories, but there are limits.

## Prerequisites

To run this project you will need:

- [Mapbox Tippecanoe](https://github.com/mapbox/tippecanoe)
- [gh-pages tool]()

These are installed within the GitHub action workflow.

## Process

What's the end to end process?

Download OS Open Zoomstack

OS Open Zoomstack is provided as a direct download link (via a redirect). The OS Data Hub download API could be used to check for new versions and download these but it is also straightforward to schedule the process to run periodically.

https://api.os.uk/downloads/v1/products/OpenZoomstack/downloads?area=GB&format=Vector+Tiles&subformat=%28MBTiles%29&redirect

Convert mbtiles to vector tiles

The mbtiles file is a SQLite database. We can use `tile-join` which is part of the Mapbox tippecanoe tool to convert this to a directory of vector tiles. Another option would be to use `mbutil`.

```bash
tile-join --output-to-directory=tiles osopenzoomstack.mbtiles --force --no-tile-size-limit
```

On a Macbook Pro M4 this process took around 5 minutes and the output directory was 2.63GB in size.

## Publish to branch

We will publish the vector tiles to a separate branch. This will keep the main branch clean and small and every time we update the branch we will force an overwrite of the history to keep the repository size down.

```bash
gh-pages -d tiles -b gh-pages -m "Update vector tiles"
```

## Compression

The vector tiles are already compressed by the tippecanoe tool. However, to serve them to a web client we would need to tell that client that they are compressed (so that the client can decompress them). Github pages does not support setting the `Content-Encoding` header, so we will need to serve the tiles via a proxy that can add this header.

For example, we could use [Cloudflare](https://www.cloudflare.com/en-gb/) to control a domain name and also to [modify the response headers](https://developers.cloudflare.com/rules/transform/response-header-modification/create-dashboard/). This would allow us to set the `Content-Encoding` header - it can also cache the tiles which would take load off GitHub.

At Geovation we use Azure API Manager to serve our vector tiles. This way we can set the `Content-Encoding` header, add a custom domain name, and control access how we wish to.

## Automation

OS Open Zoomstack is updated quarterly. This repository includes a GitHub action

## End result

At the end of this

- Repository size:
- Update frequency
- Vector tiles hosted on GitHub Pages

```

```
