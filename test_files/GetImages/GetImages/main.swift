import Foundation

//create a mutable request with api view path /viewpost, set method to POST
//kyle
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/viewpost")!)
//trenton
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.110:8000/getimages/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//parameter values
//common post information
var postid = "54"
var category = "Events"


//this is the parameters array that will be formulated as JSON.
// We need both postid and category
var params = ["post_id":postid,          //post id so we find the post
    "category":category]                 //category so we know what table to search
    as Dictionary<String,AnyObject>


//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    
    //read the message from the response
    var imageString: [String] = ["","",""]
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
    
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
    else{
        if let parseJSON = json as? Dictionary<String,UIImage>{

            //The Three images are processed here
            imageString[0] = parseJSON["image1"]! as UIImage
            imageString[1] = parseJSON["image2"]! as UIImage
            imageString[2] = parseJSON["image3"]! as String
            if !imageString[0].isEmpty {
                let imageData1 = NSData(base64EncodedString: imageString[0], options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                
                println(imageString[0])
            }
            else{
                //CASE IN WHICH THE POST HAD NO IMAGE 1
            }
            if !imageString[1].isEmpty {
                let imageData2 = NSData(base64EncodedString: imageString[1], options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                
                //do stuff with the image here
            }
            else{
                //CASE IN WHICH THE POST HAD NO IMAGE 2
            }
            if !imageString[2].isEmpty {
                let imageData3 = NSData(base64EncodedString: imageString[2], options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                
                //do stuff with the image here
            }
            else{
                //CASE IN WHICH THE POST HAD NO IMAGE 3
            }
            
        }
    }
    
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: user created, carry on!
        if(status_code == 200){
            
        }
            //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
        }
            
            //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("The server is down! Call the fire department!")
        }
        
        
    } else {
        println("Error in casting response, data incomplete")
    }
    
    
    
})
task.resume()


sleep(5)

