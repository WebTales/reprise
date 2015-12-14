from pymongo import MongoClient
import urllib2
import base64
import gridfs
import mimetypes
import time
import os
import lxml
import params
import pymysql.cursors

client = MongoClient(params.connexionString)
db = client[params.dbName]
fs = gridfs.GridFS(db)

mysqlConnection = pymysql.connect(host=params.host,
                             user=params.user,
                             password=params.password,
                             db=params.db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def insertContent(content_id, titre, resume, texte, visuel, objectType, taxo, workspace):

    # get dates
    dates = getDates(content_id)
    
    # get proper encoding
    titre = titre.encode('UTF-8')
    resume = titre
    
    # default values
    articleTypeId = "5644ac7880dd204c2a000087"
    eventTypeId = "5644b0a380dd20200f0001ce"
    createTime = int(time.time())
    lastUpdateTime = createTime
    
    # insert visuel
    if visuel is not None:
        visuel_id = str(insertDAM(visuel,titre,"Image"))
    else:
        visuel_id = None
    
    # get and replace images in body
    body_lxml = lxml.html.fromstring(texte)
    for thumbnail in body_lxml.xpath('//img[not (contains(@src, "arton") or contains(@src, "puce"))]'):
        image_src = thumbnail.get('src')
        image_id = str(insertDAM(image_src,titre,"Image"))
        image_path = '/dam?media-id=' + image_id
        thumbnail.set('src',image_path) 

    # get body
    texte = lxml.html.tostring(body_lxml, encoding='UTF-8')  
    
    # get and replace pdfs in body
    #for pdf in body_lxml.xpath('//link[@type="application/pdf"]'):
    for pdf in body_lxml.xpath('//a[contains(@href,".pdf")]'):
        pdf_src = pdf.get('href')
        pdf_id = str(insertDAM(pdf_src,titre,"Document"))
        pdf_path = '/dam?media-id=' + pdf_id
        pdf.set('href',pdf_path)

    if taxo == "" or taxo is None:
        taxo_id = None
    else:
        taxo_id = [taxo]
    
    if workspace == "":
        writeWorkspace = "global"
        target = ["global"]
    else:
        writeWorkspace = workspace
        target = ["global", workspace]
    
    if objectType == 'article':            
        object = {
            "text" : titre,
            "typeId" : articleTypeId,
            "version" : 1,
            "online" : True,
            "lastUpdateTime" : lastUpdateTime,
            "createTime" : createTime,
            "isProduct" : False,
            "productProperties" : "",
            "workspace" : {
                "fields" : {
                    "image" : visuel_id,
                    "date" : dates['date_debut']
                },
                "status" : "published",
                "startPublicationDate" : "",
                "endPublicationDate" : "",
                "taxonomy" : {
                    "navigation" : taxo_id
                },  
                "target" : target,
                "writeWorkspace" : writeWorkspace,
                "pageId" : "",
                "maskId" : "",
                "blockId" : "",
                "i18n" : {
                    "fr" : {
                        "fields" : {
                            "text" : titre,
                            "urlSegment" : "",
                            "summary" : resume,
                            "corps" : texte
                        },
                        "locale" : "fr"
                    }
                },
                "nativeLanguage" : "fr"
            },
            "live" : {
                "fields" : {
                    "image" : visuel_id
                },
                "status" : "published",
                "startPublicationDate" : "",
                "endPublicationDate" : "",
                "taxonomy" : {
                    "navigation" : taxo_id
                },                  
                "target" : target,
                "writeWorkspace" : writeWorkspace,
                "pageId" : "",
                "maskId" : "",
                "blockId" : "",
                "i18n" : {
                    "fr" : {
                        "fields" : {
                            "text" : titre,
                            "urlSegment" : "",
                            "summary" : resume,
                            "corps" : texte
                        },
                        "locale" : "fr"
                    }
                },
                "nativeLanguage" : "fr"
            },
            "lastUpdateUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            },
            "createUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            }
        }

    if objectType == 'event':         
        object = {
            "text" : titre,
            "typeId" : eventTypeId,
            "version" : 1,
            "online" : True,
            "lastUpdateTime" : lastUpdateTime,
            "createTime" : createTime,
            "isProduct" : False,
            "productProperties" : "",
            "workspace" : {
                "fields" : {
                    "image" : visuel_id,
                    "dateDebut" : dates['date_debut'],
                    "dateFin" : dates['date_fin']
                },
                "status" : "published",
                "startPublicationDate" : "",
                "endPublicationDate" : "",
                "taxonomy" : {
                    "navigation" : taxo_id
                },  
                "target" : target,
                "writeWorkspace" : writeWorkspace,
                "pageId" : "",
                "maskId" : "",
                "blockId" : "",
                "i18n" : {
                    "fr" : {
                        "fields" : {
                            "text" : titre,
                            "urlSegment" : "",
                            "summary" : resume,
                            "corps" : texte
                        },
                        "locale" : "fr"
                    }
                },
                "nativeLanguage" : "fr"
            },
            "live" : {
                "fields" : {
                    "image" : visuel_id,
                    "dateDebut" : dates['date_debut'],
                    "dateFin" : dates['date_fin']
                },
                "status" : "published",
                "startPublicationDate" : "",
                "endPublicationDate" : "",
                "taxonomy" : {
                    "navigation" : taxo_id
                },  
                "target" : target,
                "writeWorkspace" : writeWorkspace,
                "pageId" : "",
                "maskId" : "",
                "blockId" : "",
                "i18n" : {
                    "fr" : {
                        "fields" : {
                            "text" : titre,
                            "urlSegment" : "",
                            "summary" : resume,
                            "corps" : texte
                        },
                        "locale" : "fr"
                    }
                },
                "nativeLanguage" : "fr"
            },
            "lastUpdateUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            },
            "createUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            }
        }
    
    content_id = db.Contents.insert_one(object).inserted_id
    #print(object)

def getDates(content_id):
    with mysqlConnection.cursor() as cursor:
        dates = {
            'date_debut' : None,
            'date_fin' : None
        }
        # Read a single record
        sql = "SELECT date, date_redac FROM spip_articles WHERE id_article=" + content_id
        cursor.execute(sql)
        result = cursor.fetchone()
        if result['date']:
            dates['date_debut'] = int(time.mktime(result['date'].timetuple()))
        if result['date_redac']:
            dates['date_fin'] = int(time.mktime(result['date_redac'].timetuple()))
        return(dates)

def insertDAM(visuel,titre,main_filetype):

    if main_filetype == "Image":
        typeId = "51a60c1cc1c3da0407000007"
    if main_filetype == "Document":
        typeId = "5645acc380dd20200f0001e1"    
    
    fileName = os.path.basename(visuel)
    damObject = db.Dam.find_one({'title':fileName},{'_id':1})
    if (damObject is None):
        filePath = params.baseUrl + visuel
        contentType, fileEncoding =  mimetypes.guess_type(filePath)
        image = urllib2.urlopen(filePath)
        meta = image.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        ct = {
            'Content-Type': contentType
        }
        originalFileId = fs.put(image, content_type=contentType, filename=fileName, mainFileType=main_filetype, text=titre, **ct)
        createTime = int(time.time())
        lastUpdateTime = createTime
        dam = {
            "typeId" : typeId,
            "directory" : "notFiled",
            "mainFileType" : main_filetype,
            "title" : fileName,
            "taxonomy" : [ ],
            "writeWorkspace" : "global",
            "target" : ["global"],
            "originalFileId" : str(originalFileId),
            "Content-Type" : contentType,
            "nativeLanguage" : "fr",
            "i18n" : {
                "fr" : {
                    "fields" : {
                        "title" : fileName,
                        "alt" : titre
                    },
                    "locale" : "fr"
                }
            },
            "fileSize" : fileSize,
            "version" : 1,
            "lastUpdateUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            },
            "createUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            },
            "createTime" : createTime,
            "lastUpdateTime" : lastUpdateTime
        }
        dam_id = db.Dam.insert_one(dam).inserted_id
    else:
        dam_id = damObject['_id']
    return dam_id