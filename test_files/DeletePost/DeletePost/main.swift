import Foundation

//create a mutable request with api view path /deletepost/, set method to POST
//server
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/deletepost/")!)


//trenton
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/deletepost/")!)

request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

// Category and id necessary to identify post to be deleted
let category = "Services"
let id = "16"


//this is the parameters array that will be formulated as JSON.
//it has space for EVERY attribute of EVERY category.
//only fill attributes that pertain to the category
let params = ["id":id,    // id to identify post
    "category":category]  //category to identify table
    as Dictionary<String,AnyObject>


//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    //read the message from the response
    var message = ""
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
    else{
        if let parseJSON = json as? Dictionary<String,AnyObject>{
            message = parseJSON["message"] as String
        }
    }
    
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: user created, carry on!
        if(status_code == 200){
            println(message)
            println(id)
        }
            
            //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
            println(message)
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

