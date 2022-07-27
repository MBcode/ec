{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "ingestTesting.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyPjjosU+ptPN7dFOEgoc0nQ",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/gist/MBcode/42fe2dc8d7b2484c149f3683dc876d2c/ingesttesting.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# GeoCODES ingest pipeline testing:\n",
        "\n",
        "repo_counts(from sitemap) -> repo_ld_counts(from LD-cache) -> final_counts(in the endpoint)\n",
        "\n",
        "Then unit/end-to-end spot testing of crawl products, to check that code changes don't change outputs"
      ],
      "metadata": {
        "id": "JjFLT_yESujy"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Load the github.com/earthcube/earthcube_utilities \n",
        " for now the staging version"
      ],
      "metadata": {
        "id": "e0Ir7GXCSFK5"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {
        "id": "OW9a5YnT-V-0"
      },
      "outputs": [],
      "source": [
        "%load_ext rpy2.ipython\n",
        "%load_ext google.colab.data_table\n",
        "import httpimport\n",
        "with httpimport.github_repo('MBcode', 'ec'):\n",
        "  import ec"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Start by seeing how many records are expected from each repository\n",
        "To be harvested by google-datasetsearch or GeoCODES only happens if the repository has a 'sitemap.xml' listing the dataset landing pages, which have jsonld in them, that they want indexed, so the search engine can find dataset resources of interest So we start by crawling the sitemaps, (but just this time) we will only record the number of records, so we can know how many to expect from each repository, during in the next parts of the ingestion pipeline"
      ],
      "metadata": {
        "id": "ZlX0D6k4RXHh"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "named_sitemaps={ \"ssdb.iodp\": \"https://ssdb.iodp.org/dataset/sitemap.xml\",\n",
        "#\"balto\": \"http://balto.opendap.org/opendap/site_map.txt \",\n",
        "\"linked.earth\": \"http://wiki.linked.earth/sitemap.xml\",\n",
        "\"lipdverse\": \"https://lipdverse.org/sitemap.xml\",\n",
        "\"iris\": \"http://ds.iris.edu/files/sitemap.xml\",\n",
        "\"unavco\": \"https://www.unavco.org/data/doi/sitemap.xml\",\n",
        "\"ucar\": \"https://data.ucar.edu/sitemap.xml\",\n",
        "\"opencoredata\": \"http://opencoredata.org/sitemap.xml\",\n",
        "\"magic\": \"https://www2.earthref.org/MagIC/contributions.sitemap.xml\",\n",
        "#\"neotomadb\": \"http://data.neotomadb.org/sitemap.xml\",\n",
        "\"earthchem\": \"https://ecl.earthchem.org/sitemap.xml\",\n",
        "#\"xdomes\": \"https://xdomes.tamucc.edu/srr/sensorML/sitemap.xml\",\n",
        "#\"neon\": \"https://geodex.org/neon_prodcodes_sm.xml\",\n",
        "\"designsafe\": \"https://www.designsafe-ci.org/sitemap.xml \",\n",
        "\"unidata\": \"https://www.unidata.ucar.edu/sitemap.xml\",\n",
        "\"r2r\": \"https://service-dev.rvdata.us/api/sitemap/\",\n",
        "\"geocodes_demo_dataset\": \"https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/gh-pages/metadata/Dataset/sitemap.xml\",\n",
        "\"usap-dc\": \"https://www.usap-dc.org/view/dataset/sitemap.xml\",\n",
        "\"cchodo\": \"https://cchdo.ucsd.edu/sitemap.xml\",\n",
        "\"amgeo\": \"https://amgeo-dev.colorado.edu/sitemap.xml\"}\n"
      ],
      "metadata": {
        "id": "RPbcOy8sI7wB"
      },
      "execution_count": 24,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "sitemaps=list(named_sitemaps.values())\n",
        "repos=list(named_sitemaps.keys())\n",
        "#sitemaps, repos"
      ],
      "metadata": {
        "id": "j50bMih078cU"
      },
      "execution_count": 32,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "ec.setup_sitemap()"
      ],
      "metadata": {
        "id": "3hSycECGKUNP"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#sitemaps_count = ec.sitemaps_count(sitemaps)\n",
        "#sitemaps_count  #will used cached values for now"
      ],
      "metadata": {
        "id": "qfi8zXkSoLTY"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "sitemap_count"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bplXiMrFyj02",
        "outputId": "6785c9cc-e57f-4478-a755-227cffc2caa5"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'http://datadiscoverystudio.org/sitemap/CinergiSiteIndex.xml': 0,\n",
              " 'http://ds.iris.edu/files/sitemap.xml': 0,\n",
              " 'http://opencoredata.org/sitemap.xml': 83388,\n",
              " 'http://wiki.linked.earth/sitemap.xml': 18634,\n",
              " 'https://cchdo.ucsd.edu/sitemap.xml': 5040,\n",
              " 'https://data.ucar.edu/sitemap.xml': 17005,\n",
              " 'https://ecl.earthchem.org/sitemap.xml': 920,\n",
              " 'https://geodex.org/neon_prodcodes_sm.xml': 0,\n",
              " 'https://lipdverse.org/sitemap.xml': 704,\n",
              " 'https://object.cloud.sdsc.edu/v1/AUTH_85f46aa78936477d8e71b186269414e8/gleaner-summoned': 0,\n",
              " 'https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/gh-pages/metadata/Dataset/sitemap.xml': 0,\n",
              " 'https://service-dev.rvdata.us/api/sitemap/': 0,\n",
              " 'https://ssdb.iodp.org/dataset/sitemap.xml': 25241,\n",
              " 'https://www.unavco.org/data/doi/sitemap.xml': 0,\n",
              " 'https://www.unidata.ucar.edu/sitemap.xml': 211,\n",
              " 'https://www.usap-dc.org/view/dataset/sitemap.xml': 0,\n",
              " 'https://www2.earthref.org/MagIC/contributions.sitemap.xml': 0,\n",
              " 'https://xdomes.tamucc.edu/srr/sensorML/sitemap.xml': 0}"
            ]
          },
          "metadata": {},
          "execution_count": 9
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Next see how many made it into our LinkedData-cache\n",
        "Once we capture the jsonld from each landing page, we cache that LinkedData as is, and then in another RDF format: .nt ntriples, that is easier to concatenate and to load into a triplestore"
      ],
      "metadata": {
        "id": "gWjP_Hn-ReaL"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "ec.setup_s3fs()"
      ],
      "metadata": {
        "id": "t-OyECcY-o_n"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import s3fs"
      ],
      "metadata": {
        "id": "0cZ578YZ-1e_"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "oss = s3fs.S3FileSystem(\n",
        "      anon=True,\n",
        "      key=\"\",\n",
        "      secret=\"\",\n",
        "      client_kwargs = {\"endpoint_url\":\"https://oss.geodex.org\"}\n",
        "   )"
      ],
      "metadata": {
        "id": "T1r-yb8R-9oO"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "summoned =oss.ls('gleaner/summoned')\n",
        "milled =oss.ls('gleaner/milled')"
      ],
      "metadata": {
        "id": "iY6K4Qg5_ZEx"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "for repo in summoned:\n",
        "  fa=oss.ls(repo)\n",
        "  fnum=len(fa)\n",
        "  print(f'repo:{repo} has {fnum} files')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "R-yTweku_kiY",
        "outputId": "709e7a75-6518-496f-a66b-80b400a24a6e"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "repo:gleaner/summoned/amgeo has 5 files\n",
            "repo:gleaner/summoned/aquadocs has 1 files\n",
            "repo:gleaner/summoned/bco-dmo has 13221 files\n",
            "repo:gleaner/summoned/bcodmo has 12484 files\n",
            "repo:gleaner/summoned/cchdo has 4235 files\n",
            "repo:gleaner/summoned/designsafe has 352 files\n",
            "repo:gleaner/summoned/earthchem has 1549 files\n",
            "repo:gleaner/summoned/edi has 14338 files\n",
            "repo:gleaner/summoned/geocodes_demo_datasets has 8 files\n",
            "repo:gleaner/summoned/getiedadataorg has 7206 files\n",
            "repo:gleaner/summoned/hydroshare has 15297 files\n",
            "repo:gleaner/summoned/ieda has 7774 files\n",
            "repo:gleaner/summoned/iedadata has 9347 files\n",
            "repo:gleaner/summoned/iris has 63 files\n",
            "repo:gleaner/summoned/linked.earth has 696 files\n",
            "repo:gleaner/summoned/lipdverse has 698 files\n",
            "repo:gleaner/summoned/magic has 10725 files\n",
            "repo:gleaner/summoned/neon has 181 files\n",
            "repo:gleaner/summoned/ocd has 104951 files\n",
            "repo:gleaner/summoned/opencoredata has 5894 files\n",
            "repo:gleaner/summoned/opentopo has 666 files\n",
            "repo:gleaner/summoned/opentopography has 702 files\n",
            "repo:gleaner/summoned/r2r has 1 files\n",
            "repo:gleaner/summoned/ssdb has 24124 files\n",
            "repo:gleaner/summoned/ssdb.iodp has 25225 files\n",
            "repo:gleaner/summoned/ucar has 1 files\n",
            "repo:gleaner/summoned/unavco has 13022 files\n",
            "repo:gleaner/summoned/usap-dc has 880 files\n",
            "repo:gleaner/summoned/wikilinkedearth has 1 files\n",
            "repo:gleaner/summoned/wwwbco-dmoorg has 11468 files\n",
            "repo:gleaner/summoned/wwwhydroshareorg has 4195 files\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Finally see how many get into the triplestore that backs \n",
        "\n",
        "Each dataset landing page's embeded ld+json jsonld record is put into it's own graph withen the store The graph is labeled with a UniversalResourceName [URN](https://en.wikipedia.org/wiki/Uniform_Resource_Name) which is made with a template of type urn:{type}:{repo}:... So we collect all the URNs, and count how many there are for each repository If we are very lucky, the sitemap count = LD-cache count = this count, but loosing a few from errors does happen"
      ],
      "metadata": {
        "id": "GbSvdUMVRk7P"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "ec.init_sparql()\n",
        "df=ec.get_graphs()"
      ],
      "metadata": {
        "id": "dI1_tbNDK1Rl"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "df"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 442
        },
        "id": "JrPhgvndS0Ys",
        "outputId": "25631876-d64b-4a76-9b19-cdbbc67cdd22"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Warning: total number of rows (290425) exceeds max_rows (20000). Falling back to pandas display.\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                                                        g\n",
              "0       urn:gleaner2:milled:opentopography:0047cda277b...\n",
              "1       urn:gleaner2:milled:opentopography:00845ce0c33...\n",
              "2       urn:gleaner2:milled:opentopography:008970cbb2d...\n",
              "3       urn:gleaner2:milled:opentopography:00b839b8c22...\n",
              "4       urn:gleaner2:milled:opentopography:01138abe87a...\n",
              "...                                                   ...\n",
              "290420  urn:gleaner:prov:r2r:ff91af0a990b49c6fa7cd71f1...\n",
              "290421  urn:gleaner:prov:r2r:ffc3cd385505936a2df73626c...\n",
              "290422  urn:gleaner:prov:r2r:ffc9b039d7a4c355a8cadf681...\n",
              "290423  urn:gleaner:prov:r2r:ffdacfad983e5c8d8b0be4e87...\n",
              "290424               http://www.bigdata.com/rdf#nullGraph\n",
              "\n",
              "[290425 rows x 1 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-3bca6589-dbb3-43ac-93b9-2622b67ba66b\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>g</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>urn:gleaner2:milled:opentopography:0047cda277b...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>urn:gleaner2:milled:opentopography:00845ce0c33...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>urn:gleaner2:milled:opentopography:008970cbb2d...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>urn:gleaner2:milled:opentopography:00b839b8c22...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>urn:gleaner2:milled:opentopography:01138abe87a...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>290420</th>\n",
              "      <td>urn:gleaner:prov:r2r:ff91af0a990b49c6fa7cd71f1...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>290421</th>\n",
              "      <td>urn:gleaner:prov:r2r:ffc3cd385505936a2df73626c...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>290422</th>\n",
              "      <td>urn:gleaner:prov:r2r:ffc9b039d7a4c355a8cadf681...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>290423</th>\n",
              "      <td>urn:gleaner:prov:r2r:ffdacfad983e5c8d8b0be4e87...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>290424</th>\n",
              "      <td>http://www.bigdata.com/rdf#nullGraph</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>290425 rows × 1 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-3bca6589-dbb3-43ac-93b9-2622b67ba66b')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-3bca6589-dbb3-43ac-93b9-2622b67ba66b button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-3bca6589-dbb3-43ac-93b9-2622b67ba66b');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 6
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#will do in pandas, but 1st pass was w/csv dump, like:\n",
        "df.to_csv(\"graphs.csv\")"
      ],
      "metadata": {
        "id": "1Eq8jKSuVQvO"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "repoCounts=ec.os_system_(\"cut -d':' -f3,4 graphs.csv | grep milled | sort | uniq -c |sort -n\")\n",
        "repoCounts"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 91
        },
        "id": "pVHw50clTPo9",
        "outputId": "2150556c-b364-4ebe-f3d3-9038e8eaba71"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'      3 milled:geocodes_demo_datasets\\n      5 milled:amgeo\\n     83 milled:iris\\n    182 milled:neon\\n    697 milled:lipidverse\\n    842 milled:usap-dc\\n    892 milled:designsafe\\n   1379 milled:linked.earth\\n   1649 milled:r2r\\n   1806 milled:cchdo\\n   1823 milled:earthchem\\n   2615 milled:opentopography\\n   5646 milled:hydroshare\\n   7807 milled:edi\\n  10793 milled:iedadata\\n  12743 milled:magic\\n  12902 milled:bco-dmo\\n  13379 milled:ucar\\n'"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            }
          },
          "metadata": {},
          "execution_count": 21
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!cut -d':' -f3,4 graphs.csv | grep milled | sort | uniq -c |sort -n "
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8oN-IcZdR07k",
        "outputId": "7774d62a-3ea2-4131-dff1-f00f04b68915"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "      3 milled:geocodes_demo_datasets\n",
            "      5 milled:amgeo\n",
            "     83 milled:iris\n",
            "    182 milled:neon\n",
            "    697 milled:lipidverse\n",
            "    842 milled:usap-dc\n",
            "    892 milled:designsafe\n",
            "   1379 milled:linked.earth\n",
            "   1649 milled:r2r\n",
            "   1806 milled:cchdo\n",
            "   1823 milled:earthchem\n",
            "   2615 milled:opentopography\n",
            "   5646 milled:hydroshare\n",
            "   7807 milled:edi\n",
            "  10793 milled:iedadata\n",
            "  12743 milled:magic\n",
            "  12902 milled:bco-dmo\n",
            "  13379 milled:ucar\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Put in org info in store, so can query to get a table of the falloff between stages\n",
        "\n",
        "repo_counts(from sitemap) -> repo_ld_counts(from LD-cache) -> final_counts(in the endpoint)"
      ],
      "metadata": {
        "id": "ws_MDUjlbkre"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#get all counts from sitemap/etc caches\n",
        "repo_counts,repo_ld_counts,final_counts,      repo_df_loc =ec.repos2counts(repos)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "YWo0X-getKok",
        "outputId": "41844728-a37c-4f5d-f78e-27163ef1753c"
      },
      "execution_count": 26,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/ssdb.iodp.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/linked.earth.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/lipdverse.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/iris.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/unavco.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/ucar.xml\n",
            "Getting https://opencoredata.org/sitemap_1.xml\n",
            "Getting https://opencoredata.org/sitemap_2.xml\n",
            "Getting https://opencoredata.org/sitemap_3.xml\n",
            "Getting https://opencoredata.org/sitemap_0.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/magic.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/earthchem.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/designsafe.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/unidata.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/r2r.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/geocodes_demo_dataset.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/usap-dc.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/cchodo.xml\n",
            "Getting http://geocodes.ddns.net/ec/crawl/sitemaps/amgeo.xml\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "repo_counts"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CVGX_JrytQxY",
        "outputId": "bd53a77c-e61e-4301-cc0f-597e50126a6a"
      },
      "execution_count": 27,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'amgeo': 5,\n",
              " 'cchodo': 2520,\n",
              " 'designsafe': 1638,\n",
              " 'earthchem': 920,\n",
              " 'geocodes_demo_dataset': 8,\n",
              " 'iris': 28,\n",
              " 'linked.earth': 18634,\n",
              " 'lipdverse': 704,\n",
              " 'magic': 4263,\n",
              " 'opencoredata': 83388,\n",
              " 'r2r': 44007,\n",
              " 'ssdb.iodp': 25226,\n",
              " 'ucar': 17506,\n",
              " 'unavco': 5643,\n",
              " 'unidata': 202,\n",
              " 'usap-dc': 889}"
            ]
          },
          "metadata": {},
          "execution_count": 27
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "repo_ld_counts"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Lu7IqJwIvw3j",
        "outputId": "2b7d0cd3-32d4-45ce-a33a-916b248da654"
      },
      "execution_count": 28,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'amgeo': '5',\n",
              " 'aquadocs': '1',\n",
              " 'bco-dmo': '13221',\n",
              " 'bcodmo': '12484',\n",
              " 'cchdo': '4235',\n",
              " 'designsafe': '352',\n",
              " 'earthchem': '1549',\n",
              " 'edi': '14338',\n",
              " 'geocodes_demo_datasets': '8',\n",
              " 'getiedadataorg': '7206',\n",
              " 'hydroshare': '15297',\n",
              " 'ieda': '7774',\n",
              " 'iedadata': '9347',\n",
              " 'iris': '63',\n",
              " 'linked.earth': '696',\n",
              " 'lipdverse': '698',\n",
              " 'magic': '10725',\n",
              " 'neon': '181',\n",
              " 'ocd': '104951',\n",
              " 'opencoredata': '5894',\n",
              " 'opentopo': '666',\n",
              " 'opentopography': '702',\n",
              " 'r2r': '1',\n",
              " 'ssdb': '24124',\n",
              " 'ssdb.iodp': '25225',\n",
              " 'ucar': '1',\n",
              " 'unavco': '13022',\n",
              " 'usap-dc': '880',\n",
              " 'wikilinkedearth': '1',\n",
              " 'wwwbco-dmoorg': '11468',\n",
              " 'wwwhydroshareorg': '4195'}"
            ]
          },
          "metadata": {},
          "execution_count": 28
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "final_counts"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ZMEN7qZY6yef",
        "outputId": "62d806d1-8e6e-4e68-c8d4-783989b1ab79"
      },
      "execution_count": 29,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'': '7807',\n",
              " 'adata': '10793',\n",
              " 'agic': '12743',\n",
              " 'amgeo': '5',\n",
              " 'ap-dc': '842',\n",
              " 'arthchem': '1823',\n",
              " 'bco-dmo': '12902',\n",
              " 'car': '13379',\n",
              " 'cchdo': '1806',\n",
              " 'geocodes_demo_datasets': '3',\n",
              " 'hydroshare': '5646',\n",
              " 'ignsafe': '892',\n",
              " 'ked.earth': '1379',\n",
              " 'pentopography': '2615',\n",
              " 'pidverse': '697',\n",
              " 'r2r': '1649',\n",
              " 'ris': '83'}"
            ]
          },
          "metadata": {},
          "execution_count": 29
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "cmp2=ec.merge_dict_list(repo_counts,repo_ld_counts)\n",
        "#cmp2"
      ],
      "metadata": {
        "id": "7JB6mTMt624A"
      },
      "execution_count": 30,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Now bring the expected, LD-cache, and final endpoint counts \n",
        "# into one comparable place, for each repo ..\n",
        "cmp_all_stages=ec.merge_dict_list(cmp2,final_counts)\n",
        "cmp_all_stages"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LZx4V2oi7ApR",
        "outputId": "8a479d21-502e-4de7-e5f5-9991c596eae6"
      },
      "execution_count": 33,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "defaultdict(list,\n",
              "            {'': ['7807'],\n",
              "             'adata': ['10793'],\n",
              "             'agic': ['12743'],\n",
              "             'amgeo': [[5, '5'], '5'],\n",
              "             'ap-dc': ['842'],\n",
              "             'aquadocs': [['1']],\n",
              "             'arthchem': ['1823'],\n",
              "             'bco-dmo': [['13221'], '12902'],\n",
              "             'bcodmo': [['12484']],\n",
              "             'car': ['13379'],\n",
              "             'cchdo': [['4235'], '1806'],\n",
              "             'cchodo': [[2520]],\n",
              "             'designsafe': [[1638, '352']],\n",
              "             'earthchem': [[920, '1549']],\n",
              "             'edi': [['14338']],\n",
              "             'geocodes_demo_dataset': [[8]],\n",
              "             'geocodes_demo_datasets': [['8'], '3'],\n",
              "             'getiedadataorg': [['7206']],\n",
              "             'hydroshare': [['15297'], '5646'],\n",
              "             'ieda': [['7774']],\n",
              "             'iedadata': [['9347']],\n",
              "             'ignsafe': ['892'],\n",
              "             'iris': [[28, '63']],\n",
              "             'ked.earth': ['1379'],\n",
              "             'linked.earth': [[18634, '696']],\n",
              "             'lipdverse': [[704, '698']],\n",
              "             'magic': [[4263, '10725']],\n",
              "             'neon': [['181']],\n",
              "             'ocd': [['104951']],\n",
              "             'opencoredata': [[83388, '5894']],\n",
              "             'opentopo': [['666']],\n",
              "             'opentopography': [['702']],\n",
              "             'pentopography': ['2615'],\n",
              "             'pidverse': ['697'],\n",
              "             'r2r': [[44007, '1'], '1649'],\n",
              "             'ris': ['83'],\n",
              "             'ssdb': [['24124']],\n",
              "             'ssdb.iodp': [[25226, '25225']],\n",
              "             'ucar': [[17506, '1']],\n",
              "             'unavco': [[5643, '13022']],\n",
              "             'unidata': [[202]],\n",
              "             'usap-dc': [[889, '880']],\n",
              "             'wikilinkedearth': [['1']],\n",
              "             'wwwbco-dmoorg': [['11468']],\n",
              "             'wwwhydroshareorg': [['4195']]})"
            ]
          },
          "metadata": {},
          "execution_count": 33
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Now, Compare some steps against expected values\n",
        "\n",
        "from sitemap-url to the 2 parts of the LD-cache and final endpoint graph\n",
        "\n",
        "url -> jsonld (compare w/pre extracted), ntriples (compare w/pre converted),\n",
        " \n",
        " and w/graph triples\n",
        " That can be found hitting the search, via sparql_nb's ec.txt_qry(text), incl timing\n",
        "\n",
        " then other related data/tools/etc are also as expected\n",
        "\n",
        "Can compare each step in isolation, and all the way through\n",
        "\n",
        "[Some near misses still have same meaning in next step]"
      ],
      "metadata": {
        "id": "RFCsmreGFJJW"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "ec.first(repo_df_loc)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "amvYftOtFGVh",
        "outputId": "9b9c18da-5be6-4f19-81db-fd47c3b213c9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'amgeo'"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            }
          },
          "metadata": {},
          "execution_count": 6
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "read from csv table of urls and expected results, to be kept in github documention  ;either csv or org, both editable"
      ],
      "metadata": {
        "id": "XpuTRDLmero3"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#read from csv table of urls and expected results, to be kept in github documention  ;either csv or org, both editable"
      ],
      "metadata": {
        "id": "cmZu7uPohYw6"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#should/will be:\n",
        "amgeo=ec.sitemap_all_pages(sitemaps[-1])\n",
        "amgeo"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DHHE3rADHh5a",
        "outputId": "c9669658-4811-4139-d0b8-d34cfcd41e60"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "Getting https://amgeo-dev.colorado.edu/sitemap.xml\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "0    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              "1    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              "2    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              "3    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              "4    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              "Name: loc, dtype: object"
            ]
          },
          "metadata": {},
          "execution_count": 8
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "amgeo[0]"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "id": "EgBg2CHcH7ws",
        "outputId": "49501ffc-3b76-45fe-ccdd-c9a8b10181b7"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'https://amgeo-dev.colorado.edu/static/data/data-01-01-2013-12-30-00.html'"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            }
          },
          "metadata": {},
          "execution_count": 9
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "ec.init_rdflib()"
      ],
      "metadata": {
        "id": "SHEnKUC9IaWf"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#do a crawl of a url\n",
        "ld1=ec.url2jsonLD(amgeo[0])\n",
        "ld1"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Hzq2uwFcIlIL",
        "outputId": "48d58e1e-c224-4764-a855-2eb24fc26196"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'@context': 'https://schema.org/',\n",
              " '@type': 'Dataset',\n",
              " 'about': 'AMGeO Assimilative Maps',\n",
              " 'author': {'@type': 'Organization',\n",
              "  'email': 'amgeo@colorado.edu',\n",
              "  'logo': 'https://amgeo.colorado.edu/static/img/amgeosmall.svg',\n",
              "  'name': 'AMGeO'},\n",
              " 'citation': 'AMGeO Collaboration. (2019). A Collaborative Data Science Platform for the Geospace Community: Assimilative Mapping of Geospace Observations (AMGeO) v1.0.0. Zenodo. https://doi.org/10.5281/zenodo.3564914',\n",
              " 'description': 'AMGeO helps combine diverse high-latitude geospace observations. The purpose of AMGeO is to make the latest geospace data science tool accessible to scientists and students.',\n",
              " 'distribution': {'@type': 'DataDownload',\n",
              "  'contentUrl': 'https://amgeo-dev.colorado.edu/static/data/01-01-2013-12-30-00.nc',\n",
              "  'encodingFormat': 'application/x-hdf5'},\n",
              " 'keywords': ['polar ionosphere',\n",
              "  'magnetosphere-ionosphere coupling',\n",
              "  'ionospheric electrodynamics'],\n",
              " 'name': 'AMGeO Assimilative Maps for 2013-01-01T12:30:00',\n",
              " 'spatialCoverage': {'@type': 'Place',\n",
              "  'geo': {'@type': 'GeoShape',\n",
              "   'box': '49.99975367385476 0.0 88.33332306974395 360.0'}},\n",
              " 'temporalCoverage': '2013-01-01T12:30:00',\n",
              " 'url': 'https://amgeo-dev.colorado.edu/static/data/data-01-01-2013-12-30-00.html',\n",
              " 'variableMeasured': [{'@type': 'PropertyValue',\n",
              "   'name': 'Electric Field (eastward)',\n",
              "   'unitText': 'V/m'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Electric Field (equatorward)',\n",
              "   'unitText': 'V/m'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Ovation Pyme Hall Conductance',\n",
              "   'unitText': 'mho'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Ovation Pyme Pedersen Conductance',\n",
              "   'unitText': 'mho'},\n",
              "  {'@type': 'PropertyValue', 'name': 'Electric Potential', 'unitText': 'V'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Hemisphere Integrated Joule Heating',\n",
              "   'unitText': 'GW'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Joule Heating (E-field^2*Pedersen)',\n",
              "   'unitText': 'mW/m^2'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Ion Drift Velocity (eastward)',\n",
              "   'unitText': 'm/s'},\n",
              "  {'@type': 'PropertyValue',\n",
              "   'name': 'Ion Drift Velocity (equatorward)',\n",
              "   'unitText': 'm/s'}],\n",
              " 'version': 'v2_beta'}"
            ]
          },
          "metadata": {},
          "execution_count": 12
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#retrieve associated gold standard version\n",
        "ld2=ec.wget2(\"http://geocodes.ddns.net/ld/amgeo/data-01-01-2013-12-30-00.html.jsonld\",\"ld1gold.jsonld\")\n",
        "ld2"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 166
        },
        "id": "ropq97hiI1oz",
        "outputId": "f6374ea7-1b57-441c-df46-a10b8f94f6c5"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "'{\\n  \"@context\": \"https://schema.org/\",\\n  \"@type\": \"Dataset\",\\n  \"about\": \"AMGeO Assimilative Maps\",\\n  \"author\": {\\n    \"@type\": \"Organization\",\\n    \"email\": \"amgeo@colorado.edu\",\\n    \"logo\": \"https://amgeo.colorado.edu/static/img/amgeosmall.svg\",\\n    \"name\": \"AMGeO\"\\n  },\\n  \"citation\": \"AMGeO Collaboration. (2019). A Collaborative Data Science Platform for the Geospace Community: Assimilative Mapping of Geospace Observations (AMGeO) v1.0.0. Zenodo. https://doi.org/10.5281/zenodo.3564914\",\\n  \"description\": \"AMGeO helps combine diverse high-latitude geospace observations. The purpose of AMGeO is to make the latest geospace data science tool accessible to scientists and students.\",\\n  \"distribution\": {\\n    \"@type\": \"DataDownload\",\\n    \"contentUrl\": \"https://amgeo-dev.colorado.edu/static/data/01-01-2013-12-30-00.nc\",\\n    \"encodingFormat\": \"application/x-hdf5\"\\n  },\\n  \"keywords\": [\\n    \"polar ionosphere\",\\n    \"magnetosphere-ionosphere coupling\",\\n    \"ionospheric electrodynamics\"\\n  ],\\n  \"name\": \"AMGeO Assimilative Maps for 2013-01-01T12:30:00\",\\n  \"spatialCoverage\": {\\n    \"@type\": \"Place\",\\n    \"geo\": {\\n      \"@type\": \"GeoShape\",\\n      \"box\": \"49.99975367385476 0.0 88.33332306974395 360.0\"\\n    }\\n  },\\n  \"temporalCoverage\": \"2013-01-01T12:30:00\",\\n  \"url\": \"https://amgeo-dev.colorado.edu/static/data/data-01-01-2013-12-30-00.html\",\\n  \"variableMeasured\": [\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Electric Field (eastward)\",\\n      \"unitText\": \"V/m\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Electric Field (equatorward)\",\\n      \"unitText\": \"V/m\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Ovation Pyme Hall Conductance\",\\n      \"unitText\": \"mho\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Ovation Pyme Pedersen Conductance\",\\n      \"unitText\": \"mho\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Electric Potential\",\\n      \"unitText\": \"V\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Hemisphere Integrated Joule Heating\",\\n      \"unitText\": \"GW\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Joule Heating (E-field^2*Pedersen)\",\\n      \"unitText\": \"mW/m^2\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Ion Drift Velocity (eastward)\",\\n      \"unitText\": \"m/s\"\\n    },\\n    {\\n      \"@type\": \"PropertyValue\",\\n      \"name\": \"Ion Drift Velocity (equatorward)\",\\n      \"unitText\": \"m/s\"\\n    }\\n  ],\\n  \"version\": \"v2_beta\"\\n}\\n'"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            }
          },
          "metadata": {},
          "execution_count": 14
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import json\n",
        "ld1j=json.dumps(ld1, ensure_ascii=True, indent=2)\n",
        "ec.put_txtfile(\"ld1.jsonld\",ld1j)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "h323iKQEJapd",
        "outputId": "b3bd8435-56e1-4614-f635-f73273101bfa"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "2435"
            ]
          },
          "metadata": {},
          "execution_count": 24
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#for both jsonld and ntriples comparison, either via direct or ttl file or graph comparison:\n",
        "ec.diff_nt_g(\"ld1.jsonld\",\"ld1gold.jsonld\") #working on wrapper that prints out: in_both, in_first, in_second "
      ],
      "metadata": {
        "id": "PUVRXzMvJbUi"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!wc ld1.jsonld ld1gold.jsonld"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "a-3d0MkkMRsw",
        "outputId": "2ca8323f-db81-411b-b748-8cc3e295f3d9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "  80  211 2435 ld1.jsonld\n",
            "  81  211 2436 ld1gold.jsonld\n",
            " 161  422 4871 total\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#for this maybe sort keys and forgiving diff\n",
        "#!diff -wB ld1.jsonld ld1gold.jsonld |wc\n",
        "#with ntriple comparison have seen ttl help"
      ],
      "metadata": {
        "id": "GC4mcolDMuCk"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#to make sure hasn't changed w/gold stnd, look at df['lastmod']"
      ],
      "metadata": {
        "id": "kvt-3IfXU7e5"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "amgeo.to_csv(\"amgeo.csv\")\n",
        "!ls -la"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "m13MDgxhmsrF",
        "outputId": "15a1da15-bf64-4c36-eedf-d196cbd32eda"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "total 44\n",
            "drwxr-xr-x 1 root root 4096 Jul 14 16:47 .\n",
            "drwxr-xr-x 1 root root 4096 Jul 14 14:15 ..\n",
            "-rw-r--r-- 1 root root  380 Jul 14 16:47 amgeo.csv\n",
            "drwxr-xr-x 4 root root 4096 Jul  6 13:21 .config\n",
            "-rw-r--r-- 1 root root  368 Jul 14 03:50 graph.txt\n",
            "-rw-r--r-- 1 root root 2436 May  9 18:39 ld1gold.jsonld\n",
            "-rw-r--r-- 1 root root 2435 Jul 14 14:55 ld1.jsonld\n",
            "-rw-r--r-- 1 root root 5533 Jul 14 16:16 log\n",
            "drwxr-xr-x 1 root root 4096 Jul  6 13:22 sample_data\n",
            "-rw-r--r-- 1 root root  956 Jul 14 03:15 summoned.txt\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#can use this as a basis for an expected_urls.csv in https://github.com/MBcode/ec/tree/master/test \n",
        "!cat amgeo.csv"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "q41GhKHKnFd9",
        "outputId": "1e332304-7a4c-41a9-f47d-9584e234e707"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            ",loc\n",
            "0,https://amgeo-dev.colorado.edu/static/data/data-01-01-2013-12-30-00.html\n",
            "1,https://amgeo-dev.colorado.edu/static/data/data-01-06-2013-17-30-00.html\n",
            "2,https://amgeo-dev.colorado.edu/static/data/data-02-06-2013-12-30-00.html\n",
            "3,https://amgeo-dev.colorado.edu/static/data/data-02-06-2013-13-30-00.html\n",
            "4,https://amgeo-dev.colorado.edu/static/data/data-03-17-2015-18-00-00.html\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "To get a bigger sampling for ec/test/[expected_urls.csv](https://github.com/MBcode/ec/blob/master/test/expected_urls.csv) \n",
        "\n",
        "could easily take a few from each repo, at least 1/1k"
      ],
      "metadata": {
        "id": "62GptxPcYfb2"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "repo_df_loc"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "MtPQ9A-RYVpH",
        "outputId": "a2674c2d-cde8-4be8-bd7b-ebb3d52f9091"
      },
      "execution_count": 34,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'amgeo': 0    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              " 1    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              " 2    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              " 3    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              " 4    https://amgeo-dev.colorado.edu/static/data/dat...\n",
              " Name: loc, dtype: object,\n",
              " 'cchodo': 0                http://cchdo.ucsd.edu/search/map\n",
              " 1           http://cchdo.ucsd.edu/search/advanced\n",
              " 2                   http://cchdo.ucsd.edu/contact\n",
              " 3                  http://cchdo.ucsd.edu/citation\n",
              " 4                    http://cchdo.ucsd.edu/policy\n",
              "                           ...                    \n",
              " 2515      http://cchdo.ucsd.edu/cruise/49TU9107_2\n",
              " 2516    http://cchdo.ucsd.edu/cruise/316N198212_2\n",
              " 2517      http://cchdo.ucsd.edu/cruise/49TU9210_1\n",
              " 2518      http://cchdo.ucsd.edu/cruise/49TU9310_1\n",
              " 2519    http://cchdo.ucsd.edu/cruise/33AT20120419\n",
              " Name: loc, Length: 2520, dtype: object,\n",
              " 'designsafe': 0                           https://www.designsafe-ci.org\n",
              " 1                           https://fiu.designsafe-ci.org\n",
              " 2                        https://lehigh.designsafe-ci.org\n",
              " 3                         https://mechs.designsafe-ci.org\n",
              " 4                   https://oregonstate.designsafe-ci.org\n",
              "                               ...                        \n",
              " 1633               https://www.designsafe-ci.org/podcast/\n",
              " 1634                   https://www.designsafe-ci.org/faq/\n",
              " 1635               https://www.designsafe-ci.org/covid19/\n",
              " 1636    https://www.designsafe-ci.org/covid19/coronavi...\n",
              " 1637    https://www.designsafe-ci.org/conferences/2021...\n",
              " Name: loc, Length: 1638, dtype: object,\n",
              " 'earthchem': 0         https://ecl.earthchem.org/view.php?id=6\n",
              " 1        https://ecl.earthchem.org/view.php?id=65\n",
              " 2        https://ecl.earthchem.org/view.php?id=66\n",
              " 3        https://ecl.earthchem.org/view.php?id=67\n",
              " 4        https://ecl.earthchem.org/view.php?id=68\n",
              "                           ...                    \n",
              " 915    https://ecl.earthchem.org/view.php?id=2064\n",
              " 916    https://ecl.earthchem.org/view.php?id=2065\n",
              " 917    https://ecl.earthchem.org/view.php?id=2068\n",
              " 918    https://ecl.earthchem.org/view.php?id=2070\n",
              " 919    https://ecl.earthchem.org/view.php?id=2071\n",
              " Name: loc, Length: 920, dtype: object,\n",
              " 'geocodes_demo_dataset': 0    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 1    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 2    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 3    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 4    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 5    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 6    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " 7    https://raw.githubusercontent.com/earthcube/Ge...\n",
              " Name: loc, dtype: object,\n",
              " 'iris': 0                       http://ds.iris.edu/ds/products/\n",
              " 1                   http://ds.iris.edu/ds/products/emc/\n",
              " 2            http://ds.iris.edu/ds/products/eventplots/\n",
              " 3               http://ds.iris.edu/ds/products/syngine/\n",
              " 4                   http://ds.iris.edu/ds/products/gmv/\n",
              " 5        http://ds.iris.edu/ds/products/backprojection/\n",
              " 6          http://ds.iris.edu/ds/products/globalstacks/\n",
              " 7                  http://ds.iris.edu/ds/products/esec/\n",
              " 8            http://ds.iris.edu/ds/products/infrasound/\n",
              " 9                 http://ds.iris.edu/ds/products/aswms/\n",
              " 10              http://ds.iris.edu/ds/products/sws-dbs/\n",
              " 11          http://ds.iris.edu/ds/products/aftershocks/\n",
              " 12                 http://ds.iris.edu/ds/products/ears/\n",
              " 13    http://ds.iris.edu/ds/products/envelopefunctions/\n",
              " 14             http://ds.iris.edu/ds/products/eqenergy/\n",
              " 15    http://ds.iris.edu/ds/products/sourcetimefunct...\n",
              " 16    http://ds.iris.edu/ds/products/shakemoviesynth...\n",
              " 17         http://ds.iris.edu/ds/products/momenttensor/\n",
              " 18            http://ds.iris.edu/ds/products/ancc-ciei/\n",
              " 19    http://ds.iris.edu/ds/products/globalempirical...\n",
              " 20                 http://ds.iris.edu/ds/products/emtf/\n",
              " 21        http://ds.iris.edu/ds/products/noise-toolkit/\n",
              " 22            http://ds.iris.edu/ds/products/seissound/\n",
              " 23              http://ds.iris.edu/ds/products/emerald/\n",
              " 24       http://ds.iris.edu/ds/products/eventbulletins/\n",
              " 25             http://ds.iris.edu/ds/products/filmchip/\n",
              " 26          http://ds.iris.edu/ds/products/calibration/\n",
              " 27        http://ds.iris.edu/ds/products/stationdigest/\n",
              " Name: loc, dtype: object,\n",
              " 'linked.earth': 0                       http://wiki.linked.earth/Main_Page\n",
              " 1        http://wiki.linked.earth/File:Asia-BIGELS.pale...\n",
              " 2                http://wiki.linked.earth/Dataset_Tutorial\n",
              " 3           http://wiki.linked.earth/File:TutorialFig1.png\n",
              " 4           http://wiki.linked.earth/File:TutorialFig2.png\n",
              "                                ...                        \n",
              " 18629    http://wiki.linked.earth/File:TwitterPoll_Spel...\n",
              " 18630    http://wiki.linked.earth/File:TwitterPoll_Spel...\n",
              " 18631    http://wiki.linked.earth/File:TwitterPoll_Radi...\n",
              " 18632    http://wiki.linked.earth/File:TwitterPoll_Radi...\n",
              " 18633                      http://wiki.linked.earth/Newvar\n",
              " Name: loc, Length: 18634, dtype: object,\n",
              " 'lipdverse': 0      http://lipdverse.org/Temp12k/1_0_2/117_723A.Go...\n",
              " 1      http://lipdverse.org/Temp12k/1_0_2/161_976.Mar...\n",
              " 2      http://lipdverse.org/Temp12k/1_0_2/165_1002C.H...\n",
              " 3      http://lipdverse.org/Temp12k/1_0_2/2005-804-00...\n",
              " 4      http://lipdverse.org/Temp12k/1_0_2/31Lake.Eisn...\n",
              "                              ...                        \n",
              " 699    http://lipdverse.org/Temp12k/1_0_2/Yarnyshnoe....\n",
              " 700    http://lipdverse.org/Temp12k/1_0_2/Ylimysneva....\n",
              " 701    http://lipdverse.org/Temp12k/1_0_2/Zabieniec.P...\n",
              " 702    http://lipdverse.org/Temp12k/1_0_2/Zalozhtsy.B...\n",
              " 703    http://lipdverse.org/Temp12k/1_0_2/Zbudovskabl...\n",
              " Name: loc, Length: 704, dtype: object,\n",
              " 'magic': 0       https://earthref.org/MagIC/11131\n",
              " 1       https://earthref.org/MagIC/11846\n",
              " 2       https://earthref.org/MagIC/11858\n",
              " 3       https://earthref.org/MagIC/11860\n",
              " 4       https://earthref.org/MagIC/11874\n",
              "                       ...               \n",
              " 4258    https://earthref.org/MagIC/19205\n",
              " 4259    https://earthref.org/MagIC/19206\n",
              " 4260    https://earthref.org/MagIC/19207\n",
              " 4261    https://earthref.org/MagIC/19212\n",
              " 4262    https://earthref.org/MagIC/19214\n",
              " Name: loc, Length: 4263, dtype: object,\n",
              " 'opencoredata': 0        https://opencoredata.org/id/csdco/do/b7545a859...\n",
              " 1        https://opencoredata.org/id/csdco/do/b757042e7...\n",
              " 2        https://opencoredata.org/id/csdco/do/b75754032...\n",
              " 3        https://opencoredata.org/id/csdco/do/b75a7f475...\n",
              " 4        https://opencoredata.org/id/csdco/do/b75d599b0...\n",
              "                                ...                        \n",
              " 83383                  https://opencoredata.org/about.html\n",
              " 83384             https://opencoredata.org/docs/about.html\n",
              " 83385            https://opencoredata.org/docs/search.html\n",
              " 83386                  https://opencoredata.org/index.html\n",
              " 83387                 https://opencoredata.org/search.html\n",
              " Name: loc, Length: 83388, dtype: object,\n",
              " 'r2r': 0        https://dev.rvdata.us/search/fileset/100135\n",
              " 1        https://dev.rvdata.us/search/fileset/100136\n",
              " 2        https://dev.rvdata.us/search/fileset/100137\n",
              " 3        https://dev.rvdata.us/search/fileset/100138\n",
              " 4        https://dev.rvdata.us/search/fileset/100139\n",
              "                             ...                     \n",
              " 44002    https://dev.rvdata.us/search/fileset/148766\n",
              " 44003    https://dev.rvdata.us/search/fileset/148767\n",
              " 44004    https://dev.rvdata.us/search/fileset/148768\n",
              " 44005    https://dev.rvdata.us/search/fileset/148769\n",
              " 44006    https://dev.rvdata.us/search/fileset/148770\n",
              " Name: loc, Length: 44007, dtype: object,\n",
              " 'ssdb.iodp': 0                   https://ssdb.iodp.org/dataset\n",
              " 1        https://ssdb.iodp.org/dataset/?id=100001\n",
              " 2        https://ssdb.iodp.org/dataset/?id=100002\n",
              " 3        https://ssdb.iodp.org/dataset/?id=100003\n",
              " 4        https://ssdb.iodp.org/dataset/?id=100004\n",
              "                            ...                   \n",
              " 25221    https://ssdb.iodp.org/dataset/?id=128511\n",
              " 25222    https://ssdb.iodp.org/dataset/?id=128512\n",
              " 25223    https://ssdb.iodp.org/dataset/?id=128513\n",
              " 25224    https://ssdb.iodp.org/dataset/?id=128514\n",
              " 25225    https://ssdb.iodp.org/dataset/?id=128515\n",
              " Name: loc, Length: 25226, dtype: object,\n",
              " 'ucar': 0        https://data.ucar.edu/dataset/0-1-degree-paral...\n",
              " 1        https://data.ucar.edu/dataset/0-1-degree-paral...\n",
              " 2        https://data.ucar.edu/dataset/100-years-of-pro...\n",
              " 3        https://data.ucar.edu/dataset/100-years-of-pro...\n",
              " 4        https://data.ucar.edu/dataset/100-years-of-pro...\n",
              "                                ...                        \n",
              " 17501    https://data.ucar.edu/dataset/zooplankton-abun...\n",
              " 17502    https://data.ucar.edu/dataset/zooplankton-abun...\n",
              " 17503    https://data.ucar.edu/dataset/zooplankton-abun...\n",
              " 17504    https://data.ucar.edu/dataset/zooplankton-data...\n",
              " 17505    https://data.ucar.edu/dataset/zooplankton-dens...\n",
              " Name: loc, Length: 17506, dtype: object,\n",
              " 'unavco': 0        https://www.unavco.org/data/doi/10.7283/T5X928QS\n",
              " 1       https://www.unavco.org/data/doi/10.7283/0XHG-T159\n",
              " 2       https://www.unavco.org/data/doi/10.7283/2DMR-AP19\n",
              " 3       https://www.unavco.org/data/doi/10.7283/XGQB-NY54\n",
              " 4       https://www.unavco.org/data/doi/10.7283/Z1FH-4N09\n",
              "                               ...                        \n",
              " 5638     https://www.unavco.org/data/doi/10.7283/T5RX99HT\n",
              " 5639     https://www.unavco.org/data/doi/10.7283/T55719FQ\n",
              " 5640     https://www.unavco.org/data/doi/10.7283/T5X928ZX\n",
              " 5641     https://www.unavco.org/data/doi/10.7283/T590225F\n",
              " 5642     https://www.unavco.org/data/doi/10.7283/T5P55KWB\n",
              " Name: loc, Length: 5643, dtype: object,\n",
              " 'unidata': 0                          https://www.unidata.ucar.edu/\n",
              " 1                     https://www.unidata.ucar.edu/data/\n",
              " 2        https://www.unidata.ucar.edu/data/DataFlow.html\n",
              " 3      https://www.unidata.ucar.edu/software/ldm/ldm-...\n",
              " 4                https://www.unidata.ucar.edu/data/dmrc/\n",
              "                              ...                        \n",
              " 197    https://www.unidata.ucar.edu/committees/steering/\n",
              " 198    https://www.unidata.ucar.edu/committees/orient...\n",
              " 199    https://www.unidata.ucar.edu/committees/stratc...\n",
              " 200                 https://www.unidata.ucar.edu/travel/\n",
              " 201    https://www.unidata.ucar.edu/events/2009UsersW...\n",
              " Name: loc, Length: 202, dtype: object,\n",
              " 'usap-dc': 0      https://www.usap-dc.org/view/dataset/600001\n",
              " 1      https://www.usap-dc.org/view/dataset/600002\n",
              " 2      https://www.usap-dc.org/view/dataset/600003\n",
              " 3      https://www.usap-dc.org/view/dataset/600004\n",
              " 4      https://www.usap-dc.org/view/dataset/600005\n",
              "                           ...                     \n",
              " 884    https://www.usap-dc.org/view/dataset/609655\n",
              " 885    https://www.usap-dc.org/view/dataset/609656\n",
              " 886    https://www.usap-dc.org/view/dataset/609659\n",
              " 887    https://www.usap-dc.org/view/dataset/609660\n",
              " 888    https://www.usap-dc.org/view/dataset/609667\n",
              " Name: loc, Length: 889, dtype: object}"
            ]
          },
          "metadata": {},
          "execution_count": 34
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def first(l):\n",
        "  return ec.first(list(l))"
      ],
      "metadata": {
        "id": "lMPiHeJvg-zE"
      },
      "execution_count": 36,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "firsts=list(map(first,repo_df_loc.values()))\n",
        "firsts #potentially add to list of standard intermediates, to save, for later comparison\n",
        "#len(repo_df_loc)\n",
        "#repo_df_loc.keys()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "G3Co8mFegqoL",
        "outputId": "bacc9d60-6441-477c-d13a-ccfee1c7cffb"
      },
      "execution_count": 43,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['https://ssdb.iodp.org/dataset',\n",
              " 'http://wiki.linked.earth/Main_Page',\n",
              " 'http://lipdverse.org/Temp12k/1_0_2/117_723A.Godad.2011.html',\n",
              " 'http://ds.iris.edu/ds/products/',\n",
              " 'https://www.unavco.org/data/doi/10.7283/T5X928QS',\n",
              " 'https://data.ucar.edu/dataset/0-1-degree-parallel-ocean-program-pop-output-for-eastern-equatorial-indian-ocean-and-western-in',\n",
              " 'https://opencoredata.org/id/csdco/do/b7545a85958138c02a97ca54352ad4ef89309545e6e68fec0bdd52cefaa3292b.jsonld',\n",
              " 'https://earthref.org/MagIC/11131',\n",
              " 'https://ecl.earthchem.org/view.php?id=6',\n",
              " 'https://www.designsafe-ci.org',\n",
              " 'https://www.unidata.ucar.edu/',\n",
              " 'https://dev.rvdata.us/search/fileset/100135',\n",
              " 'https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/argo.json',\n",
              " 'https://www.usap-dc.org/view/dataset/600001',\n",
              " 'http://cchdo.ucsd.edu/search/map',\n",
              " 'https://amgeo-dev.colorado.edu/static/data/data-01-01-2013-12-30-00.html']"
            ]
          },
          "metadata": {},
          "execution_count": 43
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def repo2repocounts(repo):\n",
        "    rc=repo_counts.get(repo)\n",
        "    if not rc:\n",
        "        rc=1 #\n",
        "    return rc\n",
        "\n",
        "def repo_sample(repo):\n",
        "    import random\n",
        "    rcount=repo2repocounts(repo)\n",
        "    sn = int(rcount / 10000) \n",
        "    n=min(max(sn, 1),5)\n",
        "    print(f'for {repo} choose {n} from {rcount}')\n",
        "    seq=list(repo_df_loc[repo])\n",
        "    return random.sample(seq, n)"
      ],
      "metadata": {
        "id": "9k2bpWxwsjzS"
      },
      "execution_count": 56,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "expected_urls=list(map(repo_sample,repos))\n",
        "ec.flatten(expected_urls)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CO4Uz0Lhsvv8",
        "outputId": "adb571cf-f900-441c-b691-4e24414333cb"
      },
      "execution_count": 58,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "for ssdb.iodp choose 2 from 25226\n",
            "for linked.earth choose 1 from 18634\n",
            "for lipdverse choose 1 from 704\n",
            "for iris choose 1 from 28\n",
            "for unavco choose 1 from 5643\n",
            "for ucar choose 1 from 17506\n",
            "for opencoredata choose 5 from 83388\n",
            "for magic choose 1 from 4263\n",
            "for earthchem choose 1 from 920\n",
            "for designsafe choose 1 from 1638\n",
            "for unidata choose 1 from 202\n",
            "for r2r choose 4 from 44007\n",
            "for geocodes_demo_dataset choose 1 from 8\n",
            "for usap-dc choose 1 from 889\n",
            "for cchodo choose 1 from 2520\n",
            "for amgeo choose 1 from 5\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['https://ssdb.iodp.org/dataset/?id=127708',\n",
              " 'https://ssdb.iodp.org/dataset/?id=122373',\n",
              " 'http://wiki.linked.earth/LPDa97364db.temperature',\n",
              " 'http://lipdverse.org/Temp12k/1_0_2/Hypkana.Hajkova.2016.html',\n",
              " 'http://ds.iris.edu/ds/products/syngine/',\n",
              " 'https://www.unavco.org/data/doi/10.7283/T5P55KQ3',\n",
              " 'https://data.ucar.edu/dataset/ncep-fnl-operational-model-global-tropospheric-analyses-continuing-from-july-19991',\n",
              " 'https://opencoredata.org/id/csdco/do/1641417e0a54773f37333f28c5a2a6a92e671516d74f61db22b0e5060b22ca93.jsonld',\n",
              " 'https://opencoredata.org/id/csdco/do/6ab3e531c3a457eece22c664f2093b3597ac5235d437fbbb256e3b91cfe34fa1.jsonld',\n",
              " 'https://opencoredata.org/id/csdco/do/8071d43f02c5911d49f9c3891716763d1fdd83cf3cca0b46b2091379831e4a59.jsonld',\n",
              " 'https://opencoredata.org/id/csdco/do/58fd450c99452555e993e4ae782d34eb40ba48f414a640a7761ffa9eb8cd9c5a.jsonld',\n",
              " 'https://opencoredata.org/id/csdco/do/b75a7f47538b1ee478276c9f0806cc4f4ee01325cea8eac62adcd1844ed8ef7e.jsonld',\n",
              " 'https://earthref.org/MagIC/15809',\n",
              " 'https://ecl.earthchem.org/view.php?id=1572',\n",
              " 'https://www.designsafe-ci.org/data/browser/public/designsafe.storage.published/PRJ-2137',\n",
              " 'https://www.unidata.ucar.edu/software/gempak/man/parm/apxB.html',\n",
              " 'https://dev.rvdata.us/search/fileset/147162',\n",
              " 'https://dev.rvdata.us/search/fileset/128289',\n",
              " 'https://dev.rvdata.us/search/fileset/122831',\n",
              " 'https://dev.rvdata.us/search/fileset/137436',\n",
              " 'https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/nwis-sites.json',\n",
              " 'https://www.usap-dc.org/view/dataset/600073',\n",
              " 'http://cchdo.ucsd.edu/cruise/49SU9402_2',\n",
              " 'https://amgeo-dev.colorado.edu/static/data/data-01-06-2013-17-30-00.html']"
            ]
          },
          "metadata": {},
          "execution_count": 58
        }
      ]
    }
  ]
} 
