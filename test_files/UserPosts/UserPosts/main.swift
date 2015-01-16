//
//  main.swift
//  UserPosts
//
//  Created by Kyle Handy on 1/15/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//kyle
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.164.91:8000/userposts/")!)
//trenton
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/userposts/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//set username
let username = "khandy"

let params = ["username":username] //format for as Dictionary for JSON
    as Dictionary<String,AnyObject>

//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
    else{
        
        //downcast NSURLResponse object to NSHTTPURLResponse
        if let httpResponse = response as? NSHTTPURLResponse {
            
            //get the status code
            var status_code = httpResponse.statusCode
            
            //attempt to parse JSON
            if let parseJSON = json as? Dictionary<String,AnyObject> {
                
                let message = parseJSON["message"] as String
                
                //200 = OK: carry on!
                if(status_code == 200){
                    println(message)
                
                    //response code is OK, continue with parsing JSON and reading response data
                    //THIS IS WHERE RESPONSE HANDLING CODE SHOULD GO
                
                    //get all of the posts from response
                    let posts: AnyObject = parseJSON["posts"]!
                    
                    //iterate through each post
                    for i in 0...(posts.count - 1){
                        let post: AnyObject! = posts[i] //just so we don't keep re-resolving this reference
                        
                        //get the easy ones, title, display_value and post ID
                        let title = post["title"] as String
                        let display_value = post["display_value"]! as String
                        let postID = post["id"]! as Int
                        
                        
                        
                        //read imageString, base64 encoded
                        let imageString = post["image"]! as String
                        
                        //make sure there is an image...
                        if !imageString.isEmpty {
                            let imageData = NSData(base64EncodedString: imageString, options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                            
                            //THIS IS WHERE IMAGES ARE HANDLED, if there are any...
                        }
                        
                        //no image included...
                        else{
                            //NO IMAGE WITH POST
                        }
                    }
                }
                    
                //400 = BAD_REQUEST: error in creating user, display error!
                else if(status_code == 400){
                    
                    println()
                    println(message)
                }
                    
                //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
                else if(status_code == 500){
                    println("The server is down! I blame Schnagl")
                }
            }
                
            
        }
        else {
            println("Error in casting response, data incomplete")
        }
    }
    
})

task.resume()


sleep(5)

