require 'pathname'
DATA_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR / 'corral'
SCRIPTS = WRANGLE_DIR / 'scripts'
DIRS = {
    'fetched' => CORRAL_DIR / 'fetched',
    'tidied' => CORRAL_DIR / 'tidied',
    'published' => DATA_DIR,
}


AREAS = {
  'off_campus' => 'noncampus',
  'on_campus' => 'oncampus',
  'public_property' => 'publicproperty',
  'residence_hall' => 'residencehall',
}

TOPICS = {
  'arrests' => 'arrest',
  'crimes' => 'crime',
  'disciplinary_actions' => 'discipline',
  'hate_crimes' => 'hate',
}

MIN_YEAR = 2008
MAX_YEAR = 2015


def iterate_sheets()
  vals = []
  (MIN_YEAR..MAX_YEAR).each do |yr_recorded|
    AREAS.each_pair do |area, akey|
        TOPICS.each_pair do |topic, tkey|
             xlspattern = DIRS['fetched'] / "Crime#{yr_recorded}EXCEL" / "#{akey}#{tkey}*.xls*"
             xlsglobs = Pathname.glob(xlspattern, File::FNM_CASEFOLD)
             if xlsglobs.count == 0
                STDERR.puts "Rake warning: Could not find any files for pattern: #{xlspattern}"
             elsif xlsglobs.count > 1
                raise "Unexpected glob: #{xlspattern} : \n #{xlsglobs}"
             else
               vals << ({
                  :area => area,
                  :topic => topic,
                  :year_recorded => yr_recorded,
                  :srcfile => xlsglobs[0],
                  :destfile =>  DIRS['tidied'] / "#{yr_recorded}-#{area}-#{topic}.csv"})

            end
      end
    end
  end

  return vals
end

desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end


desc "Extract tidy category counts from every spreadsheet"
task :tidy_counts => [:setup] do
    iterate_sheets.each do |d|
      puts d
       sh %Q{echo  \
              #{SCRIPTS / 'extract_counts.py'} \
              #{d[:srcfile]} \
              --area #{d[:area]} \
              --topic #{d[:topic]} \
              --year-recorded #{d[:year_recorded]} \
              > #{d[:destfile]}
          }
    end
end


desc "prints a list of categories by area by topic and their counts"
task :countcats do
    TOPICS.each_key do |topic|
      sheets = iterate_sheets.select{|s| s[:topic] == topic }
      STDERR.puts("")

      sheets.each do |s|
        STDERR.puts "\t\t#{topic}\t#{s[:year_recorded]}\t#{s[:area]}"
        sh "csvcut -c category,topic < #{s[:destfile]} | sed '1d' \
                | tr '[:lower:]' '[:upper:]' | sort | uniq -c "
      end
    end
end


# desc "Compile everything"
# task :compile  => [:setup] do
#   C_FILES.each_value{|fn| Rake::Task[fn].execute() }
#   (?<=Crime)\d{4}(?=EXCEL)
# end

# desc "publish everything"
# task :publish  => [:setup] do
#   P_FILES.each_value{|fn| Rake::Task[fn].execute() }
# end


namespace :files do
end
