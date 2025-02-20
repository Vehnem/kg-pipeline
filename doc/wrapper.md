# Api

* [ ] Process - implement base execution of echo command
* ProcessConfig 
* [ ] ProcessManager: Service, maintains job list
* [ ] AMPQProcessManager: 
* HTTPProcessManager: latter
* [ ] ProcessHeartbeat: extra thread to response with joblist
* [ ] AMPQProcessHeartbeat: indicates running jobs
* HTTPProcessHeartbeat: latter

# application.conf

```properties

```

# Messages

* Heartbeat
* Task
The only thing the framework orchestrator should do is manage the input and output
* TaskResult
This is the result, what is missing is the exchange format.

```json
{
  "input": "file:///"
}
```

