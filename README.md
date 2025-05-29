This is a simple, micro-service like application which was built to educate how to use RabbitMQ in production. In this project, i have created a new RabbitMQ lazy connection
maker, and tools to consume new messages freely, via ConsumerManager declared in the file: "src/rabbitmq.../inf.../rabbitmq/setup.py". You can see those tools and fully costumize
them to use in your own production-ready application with little checks, such as pre-check if the connection is awaible. this will work effectively in your project.
