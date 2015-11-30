from pymongo import MongoClient
import urllib2
import base64
import gridfs
import mimetypes

connexionString = 'mongodb://webtales:w3bt4les2015@149.202.168.50'
dbName = 'calais'
baseUrl = 'http://www.calais.fr/'

client = MongoClient(connexionString)
db = client[dbName]
fs = gridfs.GridFS(db)

def insertContent(titre, chapeau, texte, visuel, images):

    # get proper encoding
    titre = titre.encode('UTF-8')
    chapeau = titre
    texte = texte.encode('UTF-8')
    
    # default values
    typeId = "51a60bb0c1c3dac60700000e"
    lastUpdateTime = 1448721804
    createTime = 1448721804
    
    # insert visuel
    if visuel is not None:
        insertDAM('image de test', visuel)
    
    # get images
    for image in images:
        filename = 'http://www.calais.fr/' + str(image)
        #print filename
        #print self.checksum_md5(filename)
            
    content = {
        #"_id" : ObjectId("5659bd8c1a6c7ed3238b4621"),
        "text" : titre,
        "typeId" : typeId,
        "version" : 1,
        "online" : True,
        "lastUpdateTime" : lastUpdateTime,
        "createTime" : createTime,
        "isProduct" : False,
        "productProperties" : "",
        "workspace" : {
            "fields" : {
                "image" : "5659bd871a6c7ed4238b45c4"
            },
            "status" : "published",
            "taxonomy" : [ ],
            "startPublicationDate" : "",
            "endPublicationDate" : "",
            "target" : [
                        "",
                        "global"
                        ],
                        "writeWorkspace" : "global",
                        "pageId" : "",
                        "maskId" : "",
                        "blockId" : "",
                        "i18n" : {
                            "fr" : {
                                "fields" : {
                                    "text" : titre,
                                    "urlSegment" : "url_courte",
                                    "summary" : chapeau,
                                    "body" : texte
                                },
                                "locale" : "fr"
                        }
                        },
            "nativeLanguage" : "fr"
        },
        "live" : {
            "fields" : {
                "image" : "5659bd871a6c7ed4238b45c4"
            },
            "status" : "published",
            "taxonomy" : [ ],
            "startPublicationDate" : "",
            "endPublicationDate" : "",
            "target" : [
                        "",
                        "global"
                        ],
                        "writeWorkspace" : "global",
                        "pageId" : "",
                        "maskId" : "",
                        "blockId" : "",
                        "i18n" : {
                            "fr" : {
                                "fields" : {
                                    "text" : titre,
                                    "urlSegment" : "url_courte",
                                    "summary" : chapeau,
                                    "body" : texte
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
    
    #print(content)
    #content_id = db.Contents.insert_one(content).inserted_id

def insertDAM(title, visuel):
    filePath = baseUrl + visuel
    print mimetypes.guess_type(filePath)
    #image = urllib2.urlopen(filePath)
    
    
    
    originalFileId = "5659bd871a6c7ed4238b45c1"
    contentType = "image/jpeg"
    fileSize = 453680
    createTime = 1448721799
    lastUpdateTime = 1448721799
    dam = {
        "typeId" : "51a60c1cc1c3da0407000007",
        "directory" : "notFiled",
        "mainFileType" : "Image",
        "title" : title,
        "taxonomy" : [ ],
        "writeWorkspace" : "global",
        "target" : [
            "global"
        ],
        "originalFileId" : originalFileId,
        "Content-Type" : contentType,
        "nativeLanguage" : "fr",
        "i18n" : {
            "fr" : {
                "fields" : {
                    "title" : title,
                    "alt" : ""
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

def checksum_md5(self, filename):
    try: 
        image = urllib2.urlopen(filename)
        return base64.encodestring(image.read())
    except:
        return None