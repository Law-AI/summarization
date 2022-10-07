import os
from codes import word2vec, sent_pos, quant_feats, imp_words, word_emb, pos_tags, open_words


def features(args):
    
    data_folder = args.data_path
    
    handcrafted_features = args.important_words
    postags = args.pos_tags
    
   
    if not os.path.exists(args.features_path):
        os.mkdir(args.features_path)
        
        
    if args.w2v:
        word2vec.train_word2vec(args.data_path,args.features_path)
        w2v_model = args.features_path+"word2vec_model.bin"
    else:
        w2v_model = args.word2vec_path
    
    
    
    sent_pos_folder = args.features_path+"sent-pos\\"
    if not os.path.exists(sent_pos_folder):
        os.mkdir(sent_pos_folder)
    
    print("\n\nsentence postition")
    sent_pos.run_code(data_folder, sent_pos_folder)
    
    print("\n\nQuantitative Features")
    quant_feats.run_code(data_folder, sent_pos_folder, args.features_path+"features_quant")
    
    print("\n\n Important Words Features")
    imp_words.run_code(handcrafted_features, data_folder, args.features_path+"features_impwords")
    
    print("\n\n Word Embedding Features")
    word_emb.run_code(w2v_model, data_folder, args.features_path+"features_wordemb")
    
    print("\n\n Part-of-Speech Features")
    pos_tags.run_code(postags, data_folder, args.features_path+"features_pos")
    
    print("\n\n Open Word Features")
    open_words.run_code(w2v_model, data_folder, args.features_path+"features_openword")
