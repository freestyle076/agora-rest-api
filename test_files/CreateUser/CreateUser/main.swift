import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//kyle
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/createuser/")!)
//trenton
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/createuser/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//parameter values
var username = "khandy3"
var first_name = "Kyle"
var last_name = "Handy"
var g_email = "khandy3@zagmail.gonzaga.edu"
var p_email = "k@gmail.com"
var phone = "abanana"

//prepare parameters for json serialization
var params = ["username":username, "first_name":first_name, "last_name":last_name, "gonzaga_email":g_email, "pref_email":p_email, "phone":phone] as Dictionary<String, String>

//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in

    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: user created, carry on!
        if(status_code == 200){
            println("User has been created! Good work gentlemen!")
        }
    
        //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
        
            let responseBody = NSString(data: data, encoding: NSUTF8StringEncoding)
            println(responseBody)
            

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
