package com.library.library;

import org.apache.commons.exec.CommandLine;
import org.apache.commons.exec.DefaultExecutor;
import org.apache.commons.exec.ExecuteException;
import org.apache.commons.exec.PumpStreamHandler;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;

@SpringBootApplication
public class LibraryApplication {

	public static void main(String[] args) throws IOException {
		SpringApplication.run(LibraryApplication.class, args);
		givenPythonScript_whenPythonProcessExecuted_thenSuccess();
	}


	public static void givenPythonScript_whenPythonProcessExecuted_thenSuccess()
			throws ExecuteException, IOException {
		String line = "python3 " + resolvePythonScriptPath("sinan.py");
		CommandLine cmdLine = CommandLine.parse(line);

		ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
		PumpStreamHandler streamHandler = new PumpStreamHandler(outputStream);

		DefaultExecutor executor = new DefaultExecutor();
		executor.setStreamHandler(streamHandler);

		int exitCode = executor.execute(cmdLine);
		System.out.println("Should contain script output: Hello Baeldung Readers!!"+ outputStream.toString()
				.trim());
	}

	private static String resolvePythonScriptPath(String path){
		File file = new File(path);
		return file.getAbsolutePath();
	}

}
