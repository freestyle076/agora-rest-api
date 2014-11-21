import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//kyle
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/createpost/")!)
//trenton
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/createpost/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//parameter values
var username = "tmiller12"
var description = ""
var price = "99"
var title = "Heading Home"
var category = "Rideshare"
var departure_date_time = "01 04 2011 16"
var start_location = "Spokane"
var end_location = "Yakima"
var round_trip = "1"
var return_date_time = "01 04 2011 10"
var gonzaga_email = "1"
var pref_email = "1"
var phone = "1"

//prepare parameters for json serialization
var params = ["username":username, "description":description, "price":price, "title":title, "category":category, "gonzaga_email":gonzaga_email, "pref_email":pref_email, "phone":phone, "departure_date_time":departure_date_time, "round_trip":round_trip, "return_date_time":return_date_time,"start_location":start_location,"end_location":end_location] as Dictionary<String, String>

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
