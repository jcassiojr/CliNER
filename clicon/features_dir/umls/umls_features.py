######################################################################
#  CliCon - umls_features.py                                         #
#                                                                    #
#  Willie Boag                                      wboag@cs.uml.edu #
#                                                                    #
#  Purpose: Independent UMLS module                                  #
######################################################################



from umls_cache import UmlsCache
import umls



class UMLSFeatures:


    def __init__(self):

        """
        UMLSFeatures::Constructor
        """

        # cache for the mappings of all umls lookups made
        self.umls_lookup_cache = UmlsCache()



    def IOB_prose_features(self, sentence):

        """
        UMLSFeatures::IOB_prose_features()

        @ param sentence.  A list of words
        @return            dictionary of features
        """

        features_list = []

        for word in sentence:
            features_list.append( self.features_for_word(word) )

        return features_list



    def IOB_nonprose_features(self, sentence):

        """
        UMLSFeatures::IOB_nonprose_features()

        @ param sentence.  A list of words
        @return        dictionary of features
        """

        features_list = []

        for word in sentence:
            features_list.append( self.features_for_word(word) )

        return features_list




    def features_for_word(self, word):

        """
        UMLSFeatures::features_for_word()

        @ param word.  word to lookup in UMLS database
        @return        dictionary of  word-level features
        """


        # Return value is a list of dictionaries (of features)
        features = {}

        #print '\n'
        #print word

        # Feature: UMLS Semantic Types
        cuis = umls.get_cui(self.umls_lookup_cache , word)

        # Add each CUI
        if cuis:
            for cui in cuis:
                features[('umls_cui',cui)] = 1
                #print '\tcui: ', cui
            #print


        # Feature: UMLS Semantic Type (for each word)
        mapping = umls.umls_semantic_type_word(self.umls_lookup_cache , word )

        # Add each semantic type
        if mapping:
            for concept in mapping:
                features[('umls_semantic_type_word', concept )] = 1
                #print '\t', 'semantic_type_word: ', concept
            #print

        return features



    def concept_features_for_chunk(self, sentence, ind):

        """
        UMLSFeatures::concept_features_for_sentence()

        @ param sentence. list of words from line (after flattening chunks)
        @return           dictionary of chunk-level features
        """

        #print '\n\n\n'
        #print 'concept_features_for_chunk'
        #print sentence
        #print ind

        # Return value is a list of dictionaries (of features)
        features = {}

        # UMLS features for each words
        for word in sentence[ind].split():
            word_feats = self.features_for_word(word)
            features.update(word_feats)
        

        for feature in self.enabled_concept_features_for_sentence:


            # Feature: UMLS semantic type for the sentence
            if feature == "umls_semantic_type_sentence":

                # a list of the uml semantic of the largest substring(s).
                sentence_mapping = umls.umls_semantic_type_sentence( self.umls_lookup_cache, sentence )

                # if there are no mappings
                if not sentence_mapping:
                    features[('umls_semantic_type_sentence', None ) ] = 1
                # assign the umls definitions to the vector for each word
                else:

                    for concept in sentence_mapping:
                        if concept:
                            for mapping in concept:
                                features[('umls_semantic_type_sentence' , mapping[0] ) ] = 1


            # Feature: UMLS semantic context
            if feature == "umls_semantic_context":

                # the umls definition of the largest string the word is in
                umls_semantic_context_mappings = umls.umls_semantic_context_of_words( self.umls_lookup_cache , sentence )

                # there could be multiple contexts, iterate through the sublist
                for mapping in umls_semantic_context_mappings:
                    if not mapping: continue
                    for concept in mapping:
                        features[(feature,concept)] = 1


        return features
