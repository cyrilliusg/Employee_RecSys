Recomender System for employee classification.


Problem statement:


 HR company 'X' does research all over the labor market in Russia, and one of the areas of research is the correct classification of employees according to the positions in the catalog. For many years, this task was performed manually, but due to the large amount of information, it has become more and more complex to do it manually. The company is searching for a productive, sustainable, and simple application that will be able to help researchers fill in the data correctly.



Some additional requirements:


 1) The 'X' doesn't have an IT department. Moreover, almost all workers don't know any programming languages and use only MS Office. That's why one of the main requirements is to make the app as simple as possible. The application was created by a team of two outsourced workers, so it is not going to have constant support during the work.
 2) The company doesn't have any cloud servers or powerful hardware. Due to security requirements, the model must be installed locally on the office PC's. That's why the model should be rather light from a computational perspective: both the training and inference parts should work rather quickly.


More formally:


 1) Given the dataset with N samples, every sample has its own description: his department, his unit and his position. All these descriptions are given in Russian.
 2) Every sample has it's own three responsibility level functions(for ex:func_1, func_2, func_3) and own code of the position(for ex: MAR_23_05)
 Responsibility functions describe the importance of an object(employee) according to a universal scale from the reference catalog.
 The code doesn't mean anything special, it's just an personal id of the position.
 3) The researcher's work is to match every object with his func_1, func_2, func_3. Every uniq combination of three functions gives the distinct position of an object(employee) consequently, it's own code of the position.
 Once again, every unique combination of three functions allows us to determine the code of the position distinctly.
 4) The structure of the function levels looks as the tree graph: There are about 80 functions in the first level (the size of the first-level feature set is approximately 80). Then every 1st level function has it's second level function (every func_1 has approximately 10 func_2). Every func_2 value has six func_3 values (approximately). The intersection is possible (two different i-level functions have the intersection of their sets of i+1 level functions).
 5) The description source vocabulary is not fixed.
 6) During this time, new functions (a.k.a., new classes) are going to appeal, so the model should be able to make retraining easy and automatically.
 7) The size of the func_1 set is 80; the size of the func_2 set is 250; the size of the func_2 set is 400; and the size of the position codes set is > 1600.


Approaches to solving the task:


 During the work on the project, we are going to try different approaches.
 Due to the requirements and restrictions, we are not going to solve this problem using SOTA approaches such as LLM fine-tuning or something like that, although during the research part we will try some small Transformers or RNN architectures just to reveal the potential of these approaches and to create a foundation for further reflection and research in this area.
 To satisfy the simplicity requirements, we are going to try TF-IDF, pre-trained embeddings, and simple classificators such as Logistic Regression of Support Vector Machine. As a preprocessing pipline, we are going to try stemming, lemmatization, and a custom function that is going to remove all the trash (uninformative words) from the object's description.


Ways to make a problem statement
 There are different ways to make a problem statement:
 1) The most obvious and trivial is to make a one-step classification task where position codes are used as classes.
 This statement will have bad accuracy because of the >1600 classes.
 2)Step-by-step classification. The first and main task is to determine func_1 (80 classes).
 When we know the func_1 class, we are free to choose what we are going to predict on the next stage.
 2.1) It could be func_2 level or func_3 level.
 2.2) It could be position code classes.
