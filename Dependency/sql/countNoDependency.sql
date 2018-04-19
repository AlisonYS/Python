select n.resouceName, d.bundle
from(
	select resouceName
	from(
		select resouceName, count(*) as count_num
		from (
			select resouceName, bundle, count(*) from mpaasUi_resouce_dependency where bundle != 'null' group by resouceName, bundle
		) a group by resouceName
	)b where count_num = 1 
)n, mpaasUi_resouce_dependency as d
where n.resouceName = d.resouceName
