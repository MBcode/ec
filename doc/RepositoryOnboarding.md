This will need to be a document to onboard repositories and communities.

Here was [funded project onboarding](https://docs.google.com/document/d/1aNZnWOBdDwZK6KOLf6Zu68QP9RgM3Nakxxf0sA7FhUw/edit) doc:

[Onboarding](https://docs.google.com/document/d/1hk5Y1lspB5qTVQ0rr20YEetoUhvenE2XSRudtZ-NXwY/edit#heading=h.c31noq2qy7rx) for previous office: 

[Archetypes from GleanerIO](https://github.com/gleanerio/archetype) You are a community, or a publisher… here are some tools

[Schema.org paper](https://www.inderscienceonline.com/doi/10.1504/IJBDM.2022.128449) “Schema.org for research data managers: a primer”

Ocean Sciences Best Practice: <https://github.com/adamml/ocean-best-practices-on-schema>

[github.com/ESIPFed/science-on-schema.org/.../guides/GETTING-STARTED.md](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/GETTING-STARTED.md)

Instead of getting org info in parts, make sure they have a [re3data.org](https://www.re3data.org/)/[suggest](https://www.re3data.org/suggest) ror.org/[request](https://docs.google.com/forms/d/e/1FAIpQLSdJYaMTCwS7muuTa-B_CnAtCSkKzt19lkirAKG4u7umH9Nosg/viewform) .. 

Early sketch of a decision-tree: [github.com/earthcube/ec/doc/repo_onboarding.md](https://github.com/earthcube/ec/blob/master/doc/repo_onboarding.md) 


## [TableOfContents](https://docs.google.com/document/d/1SSeh6deu5WYhTo526ZeSyZ4Mg_XpJyrvgLG7phO9YFU/edit#):

Section 1:

What does [GeoCODES](https://www.earthcube.org/geocodes)/[DeCODER](https://www.earthcube.org/decoder) do?

Section 2:

What we need from you to start

What do we need to help assess your data

What do we need to help assess your Schema.org Dataset Metadata

What we expect once we start

Evaluating your data

Section 3

What will we try to do to ‘qualify’ your information

Sessions:

Some thoughts on how this might work

- Initial contact
- Initial support of development of schema and making data available. 
- Initial loading and review of science on schema
- Moving community to production system

We need some editable location to store the information. A google sheet with a few tabs \[Who are we, Our data, Our Science on schema, Your Data in Geocodes], Template document, 

### Section 1: What is GeoCODES/DeCODER

Reasons to work with us: Making your work more [FAIR](https://www.go-fair.org/fair-principles/)

  


Link above: <https://www.earthcube.org/geocodes> starts with:

**What is GeoCODES?**

**​**

[GeoCODES](https://geocodes.earthcube.org/) is an NSF Earthcube program effort to better enable cross-domain discovery of and access to geoscience data and research tools. GeoCODES is made up of three components respectively:

- An evolving standard for exposing data called[ science on schema](https://github.com/ESIPFed/science-on-schema.org)
- A set of tools to index relevant data from partners within the Council of Data Facilities who have adopted science on schema, plus a [prototype portal](https://geocodes.earthcube.org/) to query that data
- A Resource Registry by which to [register](https://addto.earthcube.org/) and [discover](http://www.earthcube.org/resourceregistry/) relevant tools

And: <https://www.earthcube.org/decoder> starts with: 

[DeCODER](https://www.earthcube.org/decoder)


##### Democratized Cyberinfrastructure for Open Discovery to Enable Research

**Standardize how scientific data is described**

- Allow search engines for scientific data to support discoverability AND
- Facilitate the usage of the data

​The new NSF CSSI Democratized Cyberinfrastructure for Open Discovery to Enable Research (DeCODER) project will expand and extend the successful [**EarthCube GeoCODES**](https://geocodes.earthcube.org/) framework and community to unify data and tool description and reuse across geoscience domains.  ([See announcement](https://www.ncsa.illinois.edu/ncsa-leading-3-2-million-project-to-make-scientific-data-more-discoverable/).)




### Section 2: as a [form](https://docs.google.com/forms/d/19-ZpdlJughMPiqSNU_BN5b11qB30SZsQB-bta56jl5c/prefill)


#### What we need from the start,

If they have an identifier, then in future we can pull _some_ information from that. At present, this is a manual process. In the case they do not have an organization identifier, this can help them create one by gathering the information needed. (aka tag some information)

- Project name, 

  - Brief name
  - Organization identifier (optional)
  - Logo (optional)

- Contacts

  - PI/Leader
  - Datamanager/Technical
  - Others

- Description[:](https://dataoneorg.github.io/Education/bp_step/describe/)

  - What do you do

  - Keywords

  - Data

    - Does your data have metadata?
    - How many files
    - How many megabytes/gigabytes
    - what are the data types/formats
    - How frequently are is data updated/refreshed/added
    - API’s or methods (api, s3, ftp, http, etc).


- How does your community use and access your data, presently? Do the download to laptop, use from cloud, use in Community Infrastructure
- Links to how people are using your data (undergrad lab tutorials, notebooks, papers, etc)


- Web Presence

  - Website

    - Base Application (CKAN, DKAN, Geoportal)
    - Or base framework, if custom.

  - Sitemap

  - API’s, and api documentation.



There is also [github.com/ESIPFed/science-on-schema.org/guides/DataRepository.md](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/DataRepository.md)
#### * * *


#### What do we need to help assess you data

We need to assess your data, so we can understand the complexity of data used in your community. This may not need to be done by first working session, but if you can this would help direct our team.

- Data

  - Example datasets

    - Format
    - Type
    - Est size
    - Links to an example or two
    - How do community members/applications access this data


- Tools

  - Example tools

    - Name
    - Execution env
    - documentation/tutorial/paper

- Search terms

  - If you were looking for your data, how might you search for it?


#### What do we need to help assess your Schema.org Dataset Metadata


#### .

- We want to evaluate your implementation of  Science on schema
- We want to review your implementation of an XML  sitemap, or a ‘[sitegraph](https://github.com/gleanerio/scheduler/blob/3455c4c00d7f83b3ddbe659c7096c860ae38ab3d/dagster/README.md?plain=1#L192)’
- We need to have some high bandwidth conversations when we ask for revisions on the Schema or Sitemap
- We need Input on search terms that can be used to access you data

We will help you do this in a work session(s) to help your team  learn the tools, and use best practices.

Science on schema guidance… is [here](https://github.com/ESIPFed/science-on-schema.org).

If you do not yet have schema.org Dataset data on your site, here is the Science On Schema Getting Started guidance. Even if you do have science on schema, please review the latest guidance.

Now, if you have  schema.org Dataset data on your site, please test a few pages in the validator.schema.org and provide the links in the onboarding form.

If you have not developed schema.org Dataset metadata, it can look complex, but it can be minimal, initially. But we would hope that Science On Schema can be used to more fully describe your data.

**How the data and website evaluation process works.********(INSERT DECISION TREE **[**HERE**](https://github.com/earthcube/ec/blob/master/doc/repo_onboarding.md)**)**

There are tools assess your data:

- If you have JSONLD on your pages: Link to validator.schema.org

- Detailed [Evaluation](https://github.com/ESIPFed/science-on-schema.org/tree/1d5f684cd5c65c6b528c386686090e2f2af7adb6/validation) using SHACL

  - Do we have a way to do a single SHACL?

- Sitemap checker

Steps for Evaluating:

- From your site, go to a dataset HTML page

- Test a page in [validator.schema.org](https://validator.schema.org/),

  - (insert in onboarding) Links to several types of data

- Grab XML sitemap

  - Test a loc attribute  in validator.schema.org,

- Run sitemap [checker](https://www.xml-sitemaps.com/validate-xml-sitemap.html)

- (future) Evaluate in SHACL

- Communicate with team that you think you are ready. 

  - The onboarding form should have sitemap and validator.schema.org

- We will check the data, possibly make suggestions

- We will attempt to load information from the sitemap into an instance,

  - Validate that data loaded, provide basic report on the data loading (Decoder puts basic info in onboarding doc)

    - Counts of information at each stage of loading

    - What we think got lost along the way (issues with loading)

    - Summaries of what made it into the graphstore

      - Schema Types
      - Keywords
      - Variables

    - Overall quality using SHACL tool and heatmap (Future)

-   We will build a tenant user interface

  - Test UI with the test terms
  - See that dataset pages load

- When tenant is ready, 

  - We provide links to datasets, tools in the tennant ui
  - Test with keywords.
  - Approve that information is present
  - …. 


#### Associating Data with Tools and Applications.

This is under development. Basically, we need to create tool descriptions, and load them, and get them to link to your data, as appropriate.


#### * * *





### Workflow:

Do you have Science on Schema implemented? 

Yes go to step N

No go to Step 1

You have Science on Schema

- Sitemap
- Example validator.schema.org links with your 
- Testing with shacl shapes.




## 


### Section 3: What decoder/Geodes will do

What decoder tests that need to be done

Quality checks that we do to prepare for onboarding

- Sitemap, and urls
- Jsonld extraction,
- Initial qa and loading into a tenant for you to test your data
- Shacl Evaluation

Once things are running, what we plan to provide:

- Loading to production instance

  -

- Monthly Reports (under Development)

- Yearly Reports  (under Development)
 
