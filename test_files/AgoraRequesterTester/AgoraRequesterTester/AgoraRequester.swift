//
//  AgoraRequester.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation

class AgoraRequester {
    
    //base URL
    let baseURLst: String
    
    let baseHTTPSURLst: String
    
    //URL session
    var session: NSURLSession
    
    //default initializer, specifies the target URL
    init(){
        self.baseURLst  = "http://147.222.165.3:8000/"
        self.baseHTTPSURLst = "https://147.222.165.3:443/"
        self.session = NSURLSession.sharedSession()
        
    }
    
    func POST(route: String, params: Dictionary<String,AnyObject>, success: ((Dictionary<String,AnyObject>) -> Void)?, failure: ((Int) -> Void)?){
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
            
            //init request, set target URL
            var request = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + route)!)
            
            //request headers: JSON -> and <-
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            //AgoraRequest.POST uses method POST
            request.HTTPMethod = "POST"
            
            //load up JSON object into request body
            request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: nil)
            
            //form the task, use passed callback function
            var task = self.session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
                
                if let httpResponse = response as? NSHTTPURLResponse{
                    
                    let status_code = httpResponse.statusCode
                    
                    //200 OK, continue as planned
                    if status_code == 200 {
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error parsing
                        if err != nil {
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                failure!(500)
                            }
                        }
                        
                        //if callback provided run callback function with provided JSON results
                        else if success != nil {
                            success!(parseJSON!)
                        }
                        
                    }
                    
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                        //error function: 400 bad request by client
                        if failure != nil {
                            failure!(400)
                        }
                    }
                    
                    //500 server failure
                    else if status_code == 500 {
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500)
                        }
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500)
                    }
                }
            })
            
            task.resume()
            
        }
            
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58)
            }
        }
        
    }
    
}
