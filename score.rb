def map_word(word)
  return if $word_maps[word]

  map = 0b00000000000000000000000000
  word.chars.each do |c|
    map |= 1 << (c.ord - 'a'.ord)
  end

  $word_maps[word] = map
end

def letters_in_common?(word1, word2)
  map_word(word1)
  map_word(word2)

  # puts "considering #{word1} (#{$word_maps[word1].to_s(2).reverse}) and #{word2} (#{$word_maps[word2].to_s(2).reverse})"

  $word_maps[word1] & $word_maps[word2] != 0
end

def letters_in_common2?(word1, word2)
  # puts "considering #{word1} and #{word2}"

  word1.chars.each do |c1|
    # puts c1 if word2.include?(c1)
    return true if word2.include?(c1)
  end

  false
end

# Load word list into memory
words = File.readlines('words_shuf_110k.txt')

$word_maps = {}

# Sort in decreasing order of word length
words = words.sort_by(&:length).reverse

# Calculate some metrics
max_length = words.first.length

# Consider the subset of words of max_length. For each pair, see if there are
# any letters in common.
while max_length > 0
  subset = words.select { |w| w.length >= max_length }

  puts "found #{subset.length} words of length #{max_length}"

  if subset.length >= 2
    subset.each_with_index do |w, i|
      rest_of_list = subset[i + 1, subset.length - 1]
      rest_of_list.each do |w2|
        next if letters_in_common?(w.strip, w2.strip)

        puts "#{w.strip} #{w2.strip} #{w.strip.length * w2.strip.length}"
        max_length = 0
        break
      end
    end
  end

  max_length -= 1
end