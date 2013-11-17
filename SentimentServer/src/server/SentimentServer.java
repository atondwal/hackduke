package server;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.Label;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.sentiment.*;

import java.net.*;
import java.util.Properties;
import java.io.*;

public class SentimentServer {
	
	static void setSentimentLabels(Tree tree) {
		if (tree.isLeaf()) {
		      return;
		    }

		    for (Tree child : tree.children()) {
		      setSentimentLabels(child);
		    }

		    Label label = tree.label();
		    if (!(label instanceof CoreLabel)) {
		      throw new IllegalArgumentException("Required a tree with CoreLabels");
		    }
		    CoreLabel cl = (CoreLabel) label;
		    cl.setValue(Integer.toString(RNNCoreAnnotations.getPredictedClass(tree)));
	}
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		try (
	            ServerSocket serverSocket = new ServerSocket(6969);
	            Socket clientSocket = serverSocket.accept();
	            PrintWriter out =
	                new PrintWriter(clientSocket.getOutputStream(), true);
	            BufferedReader in = new BufferedReader(
	                new InputStreamReader(clientSocket.getInputStream()));
	        ) {
				Properties props = new Properties();
				props.setProperty("annotators", "tokenize, ssplit, parse, sentiment");
	         	StanfordCoreNLP analyzer = new StanfordCoreNLP(props);
	            String inputLine, outputLine;
	            
	 
	            while ((inputLine = in.readLine()) != null) {
	                if (inputLine.equals("SERVER COMMAND DIE"))
	                    break;
	                Annotation document = new Annotation(inputLine);
	                analyzer.annotate(document);
	                for(CoreMap sentence: document.get(CoreAnnotations.SentencesAnnotation.class)) {
	                	Tree tree = sentence.get(SentimentCoreAnnotations.AnnotatedTree.class);
	                	setSentimentLabels(tree);
	                	Label sentiment = tree.label();
	                	outputLine = Integer.parseInt(sentiment.value()) >= 3 ? "+": "-";
	                	outputLine += " " + sentiment.value();
	                	out.println(outputLine);
	                }
	            }
	        } catch (IOException e) {
	            System.out.println("Exception caught when trying to listen on port "
	                + 6969 + " or listening for a connection");
	            System.out.println(e.getMessage());
	        }
	}

}
