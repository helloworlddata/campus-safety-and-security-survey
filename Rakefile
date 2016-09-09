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
               xlsname = xlsglobs[0]
               destname = DIRS['tidied'] / "#{yr_recorded}-#{area}-#{topic}.csv"
               sh %Q{python \
                    #{SCRIPTS / 'extract_counts.py'} \
                    #{xlsname} \
                    --area #{area} \
                    --topic #{topic} \
                    --year-recorded #{yr_recorded} \
                    > #{destname}}

             end
        end
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
