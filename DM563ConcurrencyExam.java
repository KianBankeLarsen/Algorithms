// Default Exam.java packages
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
// My added packages
import java.nio.file.Files;
import java.util.stream.Stream;
import java.util.stream.Collectors;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.text.BreakIterator;
import java.io.IOException;

/*
This is the exam for DM563 - Concurrent Programming, Spring 2021.

Your task is to implement the following methods of class Exam:
- findUniqueWords;
- findCommonWords;
- wordLongerThan.

These methods search text files for particular words.
You must use a BreakIterator to identify words in a text file,
which you can obtain by calling BreakIterator.getWordInstance().
For more details on the usage of BreakIterator, please see the corresponding video lecture in the course.

The implementations of these methods must exploit concurrency to achieve improved performance.

The only code that you can change is the implementation of these methods.
In particular, you cannot change the signatures (return type, name, parameters) of any method, and you cannot edit method main.
The current code of these methods throws an UnsupportedOperationException: remove that line before proceeding on to the implementation.

You can find a complete explanation of the exam rules at the following webpage.

https://github.com/fmontesi/cp2021/tree/master/exam
*/
public class Exam {
	// Do not change this method
	public static void main(String[] args) {
		checkArguments(args.length > 0,
				"You must choose a command: help, findUniqueWords, findCommonWords, or wordLongerThan.");
		switch (args[0]) {
			case "help":
				System.out.println(
						"Available commands: help, findUniqueWords, findCommonWords, or wordLongerThan.\nFor example, try:\n\tjava Exam findUniqueWords data");
				break;
			case "findUniqueWords":
				checkArguments(args.length == 2, "Usage: java Exam.java findUniqueWords <directory>");
				List<LocatedWord> uniqueWords = findUniqueWords(Paths.get(args[1]));
				System.out.println("Found " + uniqueWords.size() + " unique words");
				uniqueWords.forEach(locatedWord -> System.out.println(locatedWord.word + ":" + locatedWord.filepath));
				break;
			case "findCommonWords":
				checkArguments(args.length == 2, "Usage: java Exam.java findCommonWords <directory>");
				List<String> commonWords = findCommonWords(Paths.get(args[1]));
				System.out.println("Found " + commonWords.size() + " words in common");
				commonWords.forEach(System.out::println);
				break;
			case "wordLongerThan":
				checkArguments(args.length == 3, "Usage: java Exam.java wordLongerThan <directory> <length>");
				int length = Integer.parseInt(args[2]);
				Optional<LocatedWord> longerWordOptional = wordLongerThan(Paths.get(args[1]), length);
				longerWordOptional.ifPresentOrElse(
						locatedWord -> System.out.println("Found " + locatedWord.word + " in " + locatedWord.filepath),
						() -> System.out.println("No word found longer than " + args[2]));
				break;
			default:
				System.out.println("Unrecognised command: " + args[0] + ". Try java Exam.java help.");
				break;
		}
	}

	// Do not change this method
	private static void checkArguments(Boolean check, String message) {
		if (!check) {
			throw new IllegalArgumentException(message);
		}
	}

	/**
	 * Returns all the words that appear in at most one file among all the text
	 * files contained in the given directory.
	 *
	 * This method recursively visits a directory to find text files contained in it
	 * and its subdirectories (and the subdirectories of these subdirectories,
	 * etc.).
	 *
	 * You must consider only files ending with a ".txt" suffix. You are guaranteed
	 * that they will be text files.
	 *
	 * The method should return a list of LocatedWord objects (defined by the class
	 * at the end of this file). Each LocatedWord object should consist of: - a word
	 * that appears in exactly one file (that is, the word must appear in at least
	 * one file, but not more than one); - the path to the file containing the word.
	 *
	 * All unique words must appear in the list: words that can be in the list must
	 * be in the list.
	 * 
	 * Words must be considered equal without considering differences between
	 * uppercase and lowercase letters. For example, the words "Hello", "hEllo" and
	 * "HELLo" must be considered equal to the word "hello".
	 *
	 * @param dir the directory to search
	 * @return a list of words unique to a single file
	 */

    //################################ START OF SOLUTION ###############################//

    /*
     * # This exercise is solved by using the Java 11 Stream API.
     * 
     * (1) First all filepaths are collected into a list by using Collectors,
     * since file walking doesn't parallelize well.
     * 
     * (2) A parallelStream is started to compute all files in the list.
     * For every file, all words are extracted and mapped to LocatedWord and
     * collected into a map. When a word appears in the map for the first time, 
     * it is mapped using the object field 'word' as a key and the object itself 
     * for its value, but when a word encounter the map for the second time, 
     * or more, the word is mapped to an empty optional.
     * 
     * (3) Now the only thing to do, is to remove all the empty optionals and
     * return a list of all the values of the map. This is done by walking through 
     * the set of map-values in parallel, and collecting those values that are not 
     * empty into a list. 
     */

	private static List<LocatedWord> findUniqueWords( Path dir ) {
        Map< String, Optional< LocatedWord > > uniqueWords = null;

        // Collects a map containing Locatedword as values for distinct words, 
        // else Optional.empty.
        try {
			uniqueWords = Files
                .walk( dir )
				.filter( Files::isRegularFile )
                .filter( txtFilePath -> txtFilePath.toString().endsWith( ".txt" ) )
				.collect( Collectors.toList() )
                // Creates a parallel stream pipeline.
				.parallelStream()
                .flatMap( txtFilePath -> {
                    try {
                        return Files
                            .lines( txtFilePath )
                            .flatMap( Exam::extractWords )
                            // All words are mapped to lowercase to ensure Hello and 
                            //  heLLo isn't different words.
                            .map( String::toLowerCase )
                            // Not globally distinct, only for the file being computed 
                            //  - sequential context.
                            // Distinct makes sure that recurring words within one file 
                            //  doesn't change whether a word is perceived as unique across 
                            //  files, since doublicates of words in one file otherwise will 
                            //  force the following map to merge.
                            .distinct() 
                            .map( txtWord -> new LocatedWord( txtWord, txtFilePath ) );
                    } catch (IOException e) {
                        return Stream.empty();
                    }
                } )
                // Map to distinguish duplicates from unique words.
                // ConcurrentMap is used because the official Java 11 Collectors documentation 
                //  recomonds it for parallel stream pipelines, since it is expensive to merge 
                //  the individually supplied hashMaps.
                .collect( Collectors.toConcurrentMap(
                    locatedWord -> locatedWord.word,
                    locatedWord -> Optional.of( locatedWord ),
                    ( v1, v2 ) -> Optional.empty()
                ) );
		} catch( IOException e ) {
            // Empty hashMap if error is thrown.
            uniqueWords = new HashMap<>();
			e.printStackTrace();
		}
        // Returns a list of LocatedWords after filtering out the Optional.empty values.
        return uniqueWords
            .values()
            .parallelStream()
            .collect(
                () -> new ArrayList<LocatedWord>(), 
                ( acc, wordOpt ) -> wordOpt.ifPresent( val -> acc.add( val ) ), 
                ArrayList::addAll
            );
	}

    //############################## END OF SOLUTION ##################################//

	/**
	 * Returns the words that appear at least once in every text file contained in
	 * the given directory.
	 *
	 * This method recursively visits a directory to find text files contained in it
	 * and its subdirectories (and the subdirectories of these subdirectories,
	 * etc.).
	 *
	 * You must consider only files ending with a ".txt" suffix. You are guaranteed
	 * that they will be text files.
	 *
	 * The method should return a list of words, where each word appears at least once in
	 * every file contained in the given directory.
	 *
	 * Words must be considered equal without considering differences between
	 * uppercase and lowercase letters. For example, the words "Hello", "hEllo" and
	 * "HELLo" must be considered equal to the word "hello".
	 *
	 * @param dir the directory to search
	 * @return a list of words common to all the files
	 */

    //################################ START OF SOLUTION ###############################//

    /*
     * # This exercise is solved by using the Java 11 Stream API.
     * 
     * (1) First all filepaths are collected into a list by using Collectors,
     * since file walking doesn't parallelize well.
     * 
     * (2) A parallelStream is started to compute all files in the list.
     * For every file in the list, words are extracted, mapped to lowercase and 
     * collected to a set (distinct words for the individual file being computed).
     * 
     * (3) This part is really the core of the solution. Since every file is mapped
     * to a set of words, the common words can be expressed as an intersection of all
     * word sets. The resulting reduced set will therefore express the set of common 
     * words across all files streamed. 
     * 
     * (4) Since the identify of the reduction method is null, the stream will return null
     * if the stream is empty, thus a ternary is used to instantiate the returned ArrayList 
     * correctly, by checking whether commonWords is still null -- if the stream is empty.
     */

	private static List<String> findCommonWords( Path dir ) {
        Set< String > commonWords = null;

        // Streamline producing a set containing the common words across all files.
        try {
			commonWords = Files
				.walk( dir )
				.filter( Files::isRegularFile )
                .filter( txtFilePath -> txtFilePath.toString().endsWith( ".txt" ) )
				.collect( Collectors.toList() )
                // Creates a parallel stream pipeline.
				.parallelStream()
                // Produces a set of words for every file.
                .map( txtFilePath -> {
                    try {
                        return Files
                            .lines( txtFilePath )
                            .flatMap( Exam::extractWords )
                            .map( String::toLowerCase )
                            .collect( Collectors.toSet() );
                    } catch ( IOException e ) {
                        return new HashSet< String >();
                    }
                } )
                // Intersects every set to determine common words - words that occurs 
                //  in every set.
                // No combiner is required since the types aren't switched, meaning
                //  the accumulator is used for both accumulating and combining.
                .reduce( null, ( subSet, streamSet ) -> {
                    if ( subSet == null )
                        subSet = new HashSet<String>( streamSet );
                    else
                        subSet.retainAll( streamSet );
                    return subSet;
                } );
		} catch( IOException e ) {
			e.printStackTrace();
		}

        // Returns a List with the content of the computed set 'commonWords'.
        return new ArrayList< String >( 
            commonWords != null ? commonWords : new HashSet<>() 
        );
	}

    //############################## END OF SOLUTION ##################################//

	/**
	 * Returns an Optional<LocatedWord> (see below) about a word found in the files
	 * of the given directory whose length is greater than the given length.
	 *
	 * This method recursively visits a directory to find text files contained in it
	 * and its subdirectories (and the subdirectories of these subdirectories,
	 * etc.).
	 *
	 * You must consider only files ending with a ".txt" suffix. You are guaranteed
	 * that they will be text files.
	 *
	 * The method should return an (optional) LocatedWord object (defined by the
	 * class at the end of this file), consisting of:
	 * - the word found that is longer than the given length;
	 * - the path to the file containing the word.
	 *
	 * If a word satisfying the description above can be found, then the method
	 * should return an Optional containing the desired LocatedWord. Otherwise, if
	 * such a word cannot be found, the method should return Optional.empty().
	 *
	 * This method should return *as soon as possible*: as soon as a satisfactory
	 * word is found, the method should return a result without waiting for the
	 * processing of remaining files and/or other data.
	 *
	 * @param dir    the directory to search
	 * @param length the length the word searched for must exceed
	 * @return an optional LocatedWord about a word longer than the given length
	 */

    //################################ START OF SOLUTION ###############################//

    /*
     * # This exercise is solved by using the Java 11 Stream API. 
     * 
     * (1) First all filepaths are collected into a list by using Collectors,
     * since file walking doesn't parallelize well.
     * 
     * (2) A parallelStream is started to compute all files in the list.
     * For every file in the list, words are extracted, filtered and mapped to 
     * LocatedWords. The inner-stream only computes one line at a time, since 
     * streams are always *lazy*, meaning that when creating a stream, like below, 
     * does not actually do anything before it is traversed - ensures fast termination.
     * 
     * (3) At the end, findAny is used as a terminal-short-circuting operation.
     * When findAny encounters any element, it begins to shutdown the stream - 
     * ensures that no more files than needed are processed. FindAny returns an 
     * Optional of any element consumed. If the stream is empty, an empty Optional 
     * is returned. 
     * 
     * Filter(predicate).FindAny() works very similar to anyMatch(predicate) which was 
     * introduced in the lectures -- findAny() is just more suited in this situation due
     * to its return type.
     * 
     * Note: It is not important whether the first encountered word is returned, 
     * just that any word fullfilling the requirements are returend. If ordering was 
     * needed, findFirst could be used instead, since it uses an internal strictly 
     * ordering, not necessarily wanted in a concurrent method if not required.
     */

    private static Optional<LocatedWord> wordLongerThan( Path dir, int length ) {
        Optional< LocatedWord > foundWord = null;

        // Searches for any word bigger than the given 'length' parameter, and set 
        // foundWord equal to an Optional containing the LocatedWord.
        try {
			foundWord = Files
				.walk( dir )
				.filter( Files::isRegularFile )
                .filter( txtFilePath -> txtFilePath.toString().endsWith( ".txt" ) )
				.collect( Collectors.toList() )
                // Creates a parallel stream pipeline.
				.parallelStream()
                .flatMap( txtFilePath -> {
                    try {
                        return Files
                            .lines( txtFilePath )
                            .flatMap( Exam::extractWords )
                            // filter is a barrier that only allows words of the correct 
                            //  length to pass through.
                            .filter( txtWord -> txtWord.length() > length )
                            // Mapping is done after filtering because there is no reason
                            //  to make an object of a word that is too short.
                            .map( txtWord -> new LocatedWord( txtWord, txtFilePath ) );
                    } catch (IOException e) {
                        return Stream.empty();
                    }
                } )
                // Returns any of the trivially true/emitted objects from the 
                //  inner-stream as an Optional.
                .findAny();
		} catch( IOException e ) {
            // Empty Optional is created if the try block fails.
            foundWord = Optional.empty();
			e.printStackTrace();
		}

        return foundWord;
    }

    //############################## END OF SOLUTION ##################################//

    //################### AUXILIARY METHOD AND MADETORY CLASSES #######################//

    // ! METHOD BORROWED FROM THE LECTURES // PROVIDED BY FABRIZIO MONTESI. 
    // Extracts words from a String and returns a stream of words.
    public static Stream< String > extractWords( String s ) {
        List< String > words = new ArrayList<>();
        
        BreakIterator it = BreakIterator.getWordInstance();
        it.setText( s );
        
        int start = it.first();
        int end = it.next();

        while( end != BreakIterator.DONE ) {
            String word = s.substring( start, end );
            if ( Character.isLetterOrDigit( word.charAt( 0 ) ) ) {
                words.add( word );
            }
            start = end;
            end = it.next();
        }
        
        return words.stream();
    }

	// Do not change this class
	private static class LocatedWord {
		private final String word; // the word
		private final Path filepath; // the file where the word has been found

		private LocatedWord(String word, Path filepath) {
			this.word = word;
			this.filepath = filepath;
		}
	}

	// Do not change this class
	private static class WordLocation {
		private final Path filepath; // the file where the word has been found
		private final int line; // the line number at which the word has been found

		private WordLocation(Path filepath, int line) {
			this.filepath = filepath;
			this.line = line;
		}
	}

	// Do not change this class
	private static class InternalException extends RuntimeException {
		private InternalException(String message) {
			super(message);
		}
	}
}
