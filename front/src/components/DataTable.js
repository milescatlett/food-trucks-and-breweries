import React, { useMemo } from 'react';
import { MaterialReactTable } from 'material-react-table';


export const DataTable = ({ftb}) => {
    const data = ftb
    const columns = useMemo(
        () => [
            {
                accessorKey: 'brewery',
                header: 'Brewery',
                size: 150,
            },
            {
                accessorKey: 'food_truck',
                header: 'Food Truck',
                size: 150,
            },
            {
                accessorKey: 'start',
                header: 'Start Date/Time',
                size: 150,
            },
            {
                accessorKey: 'end',
                header: 'End Date/Time',
                size: 150,
            },
        ],
        [],
    );
    return <MaterialReactTable columns={columns} data={data} />;
}

export default DataTable;