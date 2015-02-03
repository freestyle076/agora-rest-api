//
//  main.swift
//  ReportPost
//
//  Created by Kyle Handy on 1/25/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//server IP address
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/reportpost/")!)
//kyle
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/reportpost/")!)
//trenton
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/reportpost/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//parameter values
var post_id = "16"
var category = "Services"
var reporter = "khandy"

//prepare parameters for json serialization
var params = ["post_id":post_id, "category":category, "reporter":reporter] as Dictionary<String, String>

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
        
        //200 = OK: post successfully refreshed!
        if(status_code == 200){
            println(message)
        }
            
            //400 = BAD_REQUEST: error in refreshing post, display error!
        else if(status_code == 400){
            println(message)
        }
            
            //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("Internal server error")
        }
        
        
    } else {
        println("Error in casting response, data incomplete")
    }
    
    
})

task.resume()

sleep(5)